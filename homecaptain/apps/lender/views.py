import logging
from collections import OrderedDict
from datetime import datetime
from django.contrib.postgres.search import SearchVector
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import (
    generics,
    mixins,
    permissions,
    viewsets
)
from rest_framework.decorators import action
from apps.customer.models import Customer
from apps.realtor.models import Realtor
from apps.customer.serializers import CustomerRealtorUpdateSerializer
from apps.lender.serializers import LoanOfficerPortalSerializer
from apps.lender.models import LoanOfficer
from apps.event.serializers import EventSerializer
from apps.event.models import Event
from apps.util.permissions import IsLoanOfficer
from django.db.models import Count, Q, Min, Max
from django.contrib.contenttypes.models import ContentType

from apps.hcauth.models import HomeCaptainUser, Recommend, Discourage, Archive
from apps.util.utils import create_export_xlsx, get_usernames_and_emails
from apps.util.picklists import (BUYER_MILESTONES_CHOICES,
                                 BUYER_MILESTONES_CHOICES_DICTS,
                                 SELLER_MILESTONES_CHOICES,
                                 SELLER_MILESTONES_CHOICES_DICTS,
                                 MILESTONES_CHOICES, EVENT_CHOICES)
from apps.concierge.models import Concierge
from apps.concierge.serializers import ConciergeSerializer
from apps.realtor.serializers import RealtorSerializer



# Create your views here.
class LoanOfficerDashboardBuyingSellingViewSet(mixins.ListModelMixin,
                                               mixins.UpdateModelMixin,
                                               mixins.RetrieveModelMixin,
                                               viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsLoanOfficer)
    ##Note: Might want to rename this
    serializer_class = CustomerRealtorUpdateSerializer
    queryset = Customer.objects.all()
    filter_fields = ('milestones', )
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'

    DASHBOARD_PAGE = 'dashboard'
    BUYING_PAGE = 'buying'
    SELLING_PAGE = 'selling'
    PAGE = None
    
    BUYER = "Buyer"
    SELLER = "Seller"
    BOTH = "Both"

    logger = logging.getLogger('LoanOfficerDashboardBuyingSellingViewSet')

    def get_queryset(self):
        self.PAGE = self.request.data.get('page', '') or self.request.GET.get('page', '')
        seller = self.request.GET.get('seller', '') or self.PAGE == self.SELLING_PAGE
        buyer = self.request.GET.get('buyer', '') or self.PAGE == self.BUYING_PAGE
        search = self.request.GET.get('search', '')
        needs_update = self.request.GET.get('needs_update', '')
        queryset = self.queryset

        if buyer:
            queryset = queryset.filter(
                requirements__loan_officer__user=self.request.user,
                buyer_seller__in=[self.BUYER, self.BOTH])
        elif seller:
            queryset = queryset.filter(
                properties__loan_officer__user=self.request.user,
                buyer_seller__in=[self.SELLER, self.BOTH])
        elif needs_update:
            queryset = self.add_needs_update_filters(
                queryset.filter(
                    Q(properties__loan_officer__user=self.request.user)|
                    Q(requirements__loan_officer__user=self.request.user)
                )
            )
        else:
            queryset = queryset.filter(
                Q(properties__loan_officer__user=self.request.user)|
                Q(requirements__loan_officer__user=self.request.user))
        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name'),
            ).filter(search__icontains=search\
            ).filter(
                Q(properties__loan_officer__user=self.request.user)|
                Q(requirements__loan_officer__user=self.request.user)
            )
        #requirements__loan_officer__user=self.request.user)
        if self.request.GET.get('milestones', '') != 'Archived' and self.action != 'restore':
            queryset = queryset.exclude(milestones='Archived')
        self.logger.debug('Customers found: ' + str(queryset.distinct().count()))
        return queryset.distinct()

    def add_needs_update_filters(self, queryset):
        return queryset.filter(update_history__is_updated=False)

    @action(detail=True, methods=['PATCH',],
            url_path='status-update', url_name='loan-officer-customer-status-update')
    def status_update(self, request, *args, **kwargs):
        if not self.request.data.get('milestones', None):
            self.logger.error("'milestones', this field is required")
            raise Exception("'milestones', this field is required")
        customer = self.get_object()
        customer.close_update_request(self.request.data['milestones'], user=self.request.user)
        return Response({
            "milestones": self.request.data['milestones']
        })

    @action(detail=False, methods=['GET',],
            url_path='export-customers',
            url_name='loan-officer-export-customers')
    def export_customers(self, request):
        uids = [uid for uid in request.GET.get('uids', '').strip().split(',') if uid]
        if uids:
            customers_data = self.get_serializer(
                self.get_queryset().filter(uid__in=uids), many=True).data
            headers = OrderedDict({
                'UID': 'uid',
                'Milestones': 'milestones',
                'Username': 'user__username',
                'First Name': 'user__first_name',
                'Last Name': 'user__last_name',
                'Phone': 'user__phone',
                'Email': 'user__email',
                'Country': 'user__address__country',
            })
            seller = request.GET.get('seller', '')
            if seller:
                report_name = "LoanOfficer-Sellers-Export"
            else:
                report_name = "LoanOfficer-Buyers-Export"
            self.logger.info('Creating output report ' + report_name)
            return create_export_xlsx(report_name, headers, customers_data)
        return Response({
            "detail": "Send GET request with query param `uids`, with values separate by commas. `uid` is `customer.uid`",
        })    

    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='loan-officer-dashboard-customer-stats')
    def stats(self, request, *args, **kwargs):
        qs = self.queryset.filter(
            Q(properties__loan_officer__user=self.request.user)|
            Q(requirements__loan_officer__user=self.request.user)
        ).distinct()
        self.PAGE = self.request.data.get('page', '') or self.request.GET.get('page', '')
        result = {}
        if self.PAGE == self.DASHBOARD_PAGE:
            milestone_choices = dict(MILESTONES_CHOICES)
            result.update({
                'BUYER_MILESTONES_CHOICES': BUYER_MILESTONES_CHOICES_DICTS,
                'SELLER_MILESTONES_CHOICES': SELLER_MILESTONES_CHOICES_DICTS,
            })
        elif self.PAGE == self.BUYING_PAGE:
            milestone_choices = dict(BUYER_MILESTONES_CHOICES)
            result.update({
                'BUYER_MILESTONES_CHOICES': BUYER_MILESTONES_CHOICES_DICTS,
            })
        elif self.PAGE == self.SELLING_PAGE:
            milestone_choices = dict(SELLER_MILESTONES_CHOICES)
            result.update({
                'SELLER_MILESTONES_CHOICES': SELLER_MILESTONES_CHOICES_DICTS,
            })
        else:
            error = "`page` is mandatory, it has to be included in the request as query param or in data. "
            error += "Possible values for page are  `%s`, `%s` and `%s`" % (self.DASHBOARD_PAGE, self.BUYING_PAGE, self.SELLING_PAGE)
            self.logger.info(error)
            return Response({
                "error": error
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # FIXME currently using customer_ids previously queried to remove duplicates
        # Maybe will be fixed with more optimized way
        customer_ids = list(qs.values_list('id', flat=True))
        stats = list(self.queryset.filter(id__in=customer_ids).values('milestones').annotate(Count('milestones')))
        
        milestones_in_db = list(qs.values_list('milestones', flat=True).distinct())
            
        for milestone_choice in milestone_choices:
            if milestone_choice not in milestones_in_db:
                stats.append({
                    'milestones': milestone_choice,
                    'milestones_display': milestone_choices[milestone_choice],
                    'milestones__count': 0
                })
        for milestone in stats:
            if milestone['milestones'] == '':
                continue
            milestone['milestones_display'] = milestone_choices[milestone['milestones']]
        counts_qs = qs.exclude(milestones='Archived')
        result['filters'] = stats
        if self.PAGE == self.DASHBOARD_PAGE:
            result['counts'] = {
                'buyers': counts_qs.filter(buyer_seller__in=[self.BUYER, self.BOTH]).count(),
                'sellers': counts_qs.filter(buyer_seller__in=[self.SELLER, self.BOTH]).count(),
                'all': counts_qs.count(),
                'needs_update': self.add_needs_update_filters(counts_qs).count()
            }
        return Response(result)

    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='loan-officer-home-customer-archive')
    def archive(self, request, *args, **kwargs):
        customer = self.get_object()
        loan_officer = self.request.user.loan_officer
        customer.milestones = 'Archived'
        customer.save()

        if customer.buyer_seller == self.BUYER or customer.buyer_seller == self.BOTH:
            for requirement in customer.requirements.all():
                loan_officer.add_requirement_to_archive(requirement.id)
        
        if customer.buyer_seller == self.SELLER or customer.buyer_seller == self.BOTH:
            for prop in customer.properties.all():
                loan_officer.add_property_to_archive(prop.id)
        self.logger.info('Archived customer %s' % customer.user.username)
        return Response({'message': 'Archived customer %s' % customer.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='loan-officer-home-customer-restore')
    def restore(self, request, *args, **kwargs):
        customer = self.get_object()
        loan_officer = self.request.user.loan_officer
        customer.milestones = 'Searching Reset'
        customer.save()

        if customer.buyer_seller == self.BUYER or customer.buyer_seller == self.BOTH:
            for requirement in customer.requirements.all():
                loan_officer.remove_requirement_from_archive(requirement.id)
        
        if customer.buyer_seller == self.SELLER or customer.buyer_seller == self.BOTH:
            for prop in customer.properties.all():
                loan_officer.remove_property_from_archive(prop.id)
        self.logger.info('Restored customer %s' % customer.user.username)
        return Response({'message': 'Restored customer %s' % customer.user.username})

class LoanOfficerProfileViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsLoanOfficer)
    queryset = LoanOfficer.objects.all()
    serializer_class = LoanOfficerPortalSerializer
    logger = logging.getLogger('LoanOfficerProfileViewSet')

    ##TODO: Later abstract this is a base HCGenericViewSet class which inherits from
    ##viewsets.GenericViewSet and all our viewsets use that HCGenericViewSet as the last
    ##parent class
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        loan_officer = request.user.loan_officer
        serializer = self.get_serializer(loan_officer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        loan_officer = request.user.loan_officer
        serializer = self.get_serializer(loan_officer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def partial_update(self, request, *args, **kwargs):
        loan_officer = request.user.loan_officer
        serializer = self.get_serializer(loan_officer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        self.logger.info(serializer.errors)
        return Response(serializer.errors)
    
class LoanOfficerDashboardEventSlotViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsLoanOfficer)
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    pagination_class = None
    logger = logging.getLogger('LoanOfficerDashboardEventSlotViewSet')

    def get_queryset(self):
        queryset = self.queryset.filter(
            Q(requested_by=self.request.user)|
            Q(additional_attendees__in=[self.request.user,])|
            Q(property__loan_officer__user=self.request.user)).distinct()
        return queryset
    
    def augment_request_data(self, request_data):
        additional_attendees = request_data.pop('additional_attendees')
        usernames, emails = get_usernames_and_emails(additional_attendees)

        request_data['additional_attendees'] = []
        for username in usernames:
            try:
                user = HomeCaptainUser.objects.get(username=username)
                request_data['additional_attendees'].append(user.pk)
            except HomeCaptainUser.DoesNotExist:
                continue
        request_data['emails'] = emails
        if request_data.get('buyer'):
            ##Note: Not silencing this exception because the UI should already be sending validated
            ##usernames and if it's still invalid, it should speak out loud  as a programming error!
            request_data['buyer'] = HomeCaptainUser.objects.get(
                username=request_data.pop('buyer').strip().strip('@')).pk

        return request_data

    def augment_serializer_data(self, serializer_data):
        if serializer_data.get('buyer'):
            ##this should speak out loud if the id is not found, so not silencing
            serializer_data['buyer'] = HomeCaptainUser.objects.get(
                id=serializer_data['buyer']).username
        if serializer_data.get('additional_attendees'):
            additional_attendees = []
            for attendee in serializer_data['additional_attendees']:
                additional_attendees.append(HomeCaptainUser.objects.get(
                    id=attendee).username)
            serializer_data['additional_attendees'] = additional_attendees
        return serializer_data

    def list(self, request, *args, **kwargs):
        serialized_list = self.serializer_class(self.get_queryset(), many=True)
        serialized_list_data = serialized_list.data
        for item in serialized_list_data:
            self.augment_serializer_data(item)
        return Response(serialized_list_data)
        
    def retrieve(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(self.get_object()).data
        self.augment_serializer_data(serialized_data)
        return Response(serialized_data)
    
    def create(self, request, *args, **kwargs):
        request_data = self.augment_request_data(request.data)
        serializer = self.get_serializer(data = request_data)
        if serializer.is_valid(): #raise_exception=True):
            self.perform_create(serializer)
            serializer_data = self.augment_serializer_data(serializer.data)
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        else:
            self.logger.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        request_data = self.augment_request_data(request.data)
        serializer = self.get_serializer(self.get_object(), data = request_data)
        if serializer.is_valid(): #raise_exception=True):
            self.perform_update(serializer)
            serializer_data = self.augment_serializer_data(serializer.data)
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        else:
            self.logger.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['GET',],
            url_path='extras', url_name='loan-officer-dashboard-agenda-extras')
    def extras(self, request, *args, **kwargs):
        return Response({
            'event_names': [e[0] for e in EVENT_CHOICES],
            'buyers': request.user.loan_officer\
            .requirements.values_list('customer__user__username', flat=True),
            'addresss': request.user.loan_officer\
            .property_set.values_list('address__street', 'id')
        })


class LoanOfficerMyConciergeViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsLoanOfficer)
    serializer_class = ConciergeSerializer
    queryset = Concierge.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('LoanOfficerMyConciergeViewSet')
    
    def get_queryset(self):
        loan_officer = self.request.user.loan_officer
        search = self.request.GET.get('search', '')
        prior = self.request.GET.get('prior', '')
        if self.action == 'archived':
            return self.queryset.filter(id__in=loan_officer.archived_concierges.\
                                        values_list('archived_object_id', flat=True))
        if prior:
            queryset = self.queryset.filter(id__in=loan_officer.archived_concierges.\
                                        values_list('archived_object_id', flat=True))
            return queryset
        else:
            queryset = self.queryset.filter(
                requirement__loan_officer__user=self.request.user).distinct()
        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name'),
            ).filter(search__icontains=search)

        if self.action != 'restore':
            queryset = queryset.exclude(id__in=loan_officer.archived_concierges.\
                                        values_list('archived_object_id', flat=True))     
        return queryset.distinct()


    def get_object(self):
        ##NOTE: HAD TO OVERRIDE THIS
        ##the filtered and difference'd queryset from get_object
        ##return's 2 objects for a given LO uid on a .get(uid=uid) call
        ##so used a get_object_or_404
        return get_object_or_404(Concierge, uid=self.kwargs['uid'])    
    
    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='loan-officer-concierge-stats')
    def stats(self, request, *args, **kwargs):
        return Response({
            'current': self.get_queryset().count(),
            'prior_count': self.request.user.loan_officer.\
            archived_concierges.count(),
        })
    
    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='loan-officer-concierge-archived')
    def archived(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        for con in serializer.data:
            concierge = Concierge.objects.get(id=con['id'])
            con.update({
                'loan_officer_users': concierge.get_loan_officer_customers(
                    request.user.loan_officer.id)
            })

        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)


    def _recommend_discourage_dry(self, receivers):
        usernames = []
        emails = []
        for item in receivers:
            item = item.strip()
            if item.startswith('@'):
                usernames.append(item.strip('@'))
            else:
                try:
                    validate_email(item)
                    emails.append(item)
                except ValidationError:
                    continue
        return usernames, emails
    
        
    @action(detail=True, methods=['POST',],
            url_path='discourage', url_name='loan-officer-concierge-discourage')
    def discourage(self, request, *args, **kwargs):
        concierge = self.get_object()
        loan_officer = self.request.user.loan_officer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        discourage, created = Discourage.objects.update_or_create(
            discouraging_content_type=ContentType.objects.get_for_model(loan_officer),
            discouraging_object_id = loan_officer.id,
            discouraged_content_type=ContentType.objects.get_for_model(concierge),
            discouraged_object_id = concierge.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails,
                'comments' : request.data.get('comments', '')
            })
        discourage.users_discouraged_to.add(*list(HomeCaptainUser.objects.\
                                                  filter(username__in=usernames)))
        self.logger.info('Successfully discouraged the Concierge ' + concierge.user.username)
        return Response({
            'discourage_count': Discourage.objects.filter(
                discouraged_content_type=ContentType.objects.get_for_model(concierge),
                discouraged_object_id = concierge.id).count(),
            'message': 'Successfully discouraged the Concierge'
        })


    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='loan-officer-concierge-recommend')
    def recommend(self, request, *args, **kwargs):
        concierge = self.get_object()
        loan_officer = self.request.user.loan_officer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(loan_officer),
            recommending_object_id = loan_officer.id,
            recommended_content_type=ContentType.objects.get_for_model(concierge),
            recommended_object_id = concierge.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails,
                'comments' : request.data.get('comments', '')
            })
        recommend.users_recommended_to.add(*list(HomeCaptainUser.objects.\
                                                 filter(username__in=usernames)))
        self.logger.info('Successfully recommend the Concierge ' + concierge.user.username)
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(concierge),
                recommended_object_id = concierge.id).count(),
            'message': 'Successfully recommend the Concierge'
        })
    
    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='loan-officer-concierge-archive')
    def archive(self, request, *args, **kwargs):
        concierge = self.get_object()
        loan_officer = self.request.user.loan_officer
        loan_officer.add_concierge_to_archive(concierge.id)
        loan_officer.save()
        self.logger.info('Archived concierge %s' % \
                         concierge.user.username)
        return Response({'message': 'Archived concierge %s' % \
                         concierge.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='loan-officer-concierge-unarchive')
    def restore(self, request, *args, **kwargs):
        ##FIXME: change to restore @brenton and let @kan101 know
        concierge = self.get_object()
        loan_officer = self.request.user.loan_officer
        loan_officer.remove_concierge_from_archive(concierge.id)
        loan_officer.save()
        self.logger.info('Restored concierge %s' % \
                         concierge.user.username)
        return Response({'message': 'Restored concierge %s' % \
                         concierge.user.username})
    
    @action(detail=False, methods=['GET',],
            url_path='export-concierges',
            url_name='loan-officer-export-concierges')
    def export_concierges(self, request):
        uids = [uid for uid in request.GET.get('uids', '').strip().split(',') if uid]
        if uids:
            concierges_data = self.get_serializer(
                self.get_queryset().filter(uid__in=uids), many=True).data
            headers = OrderedDict({
                'UID': 'uid',
                'Username': 'user__username',
                'First Name': 'user__first_name',
                'Last Name': 'user__last_name',
                'Phone': 'user__phone',
                'Email': 'user__email',
                'Country': 'user__country',
            })
            report_name = "LoanOfficer-Concierges-Export"
            self.logger.info('Creating report ' + report_name)
            return create_export_xlsx(report_name, headers, concierges_data)
        return Response({
            "detail": "Send GET request with query param `uids`, with values separate by commas. `uid` is `concierge.uid`",
        })    

class LoanOfficerMyRealtorViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsLoanOfficer)
    serializer_class = RealtorSerializer
    queryset = Realtor.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('LoanOfficerMyRealtorViewSet')
    
    def get_queryset(self):
        loan_officer = self.request.user.loan_officer
        search = self.request.GET.get('search', '')
        prior = self.request.GET.get('prior', '')
        if self.action == 'archived':
            return self.queryset.filter(id__in=loan_officer.archived_realtors.\
                                        values_list('archived_object_id', flat=True))
        if prior:
            queryset = self.queryset.filter(id__in=loan_officer.archived_realtors.\
                                        values_list('archived_object_id', flat=True))
            return queryset
        else:
            queryset = self.queryset.filter(
                requirement__loan_officer__user=self.request.user).distinct()
        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name'),
            ).filter(search__icontains=search)

        if self.action != 'restore':
            queryset = queryset.exclude(id__in=loan_officer.archived_realtors.\
                                        values_list('archived_object_id', flat=True))     
        return queryset.distinct()


    def get_object(self):
        ##NOTE: HAD TO OVERRIDE THIS
        ##the filtered and difference'd queryset from get_object
        ##return's 2 objects for a given LO uid on a .get(uid=uid) call
        ##so used a get_object_or_404
        return get_object_or_404(Realtor, uid=self.kwargs['uid'])    
    
    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='loan-officer-realtor-stats')
    def stats(self, request, *args, **kwargs):
        return Response({
            'current': self.get_queryset().count(),
            'prior_count': self.request.user.loan_officer.\
            archived_realtors.count(),
        })
    
    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='loan-officer-realtor-archived')
    def archived(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        for realtors_data in serializer.data:
            realtor = Realtor.objects.get(id=realtors_data['id'])
            realtors_data.update({
                'loan_officer_users': realtor.get_loan_officer_customers(
                    request.user.loan_officer.id)
            })

        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)


    def _recommend_discourage_dry(self, receivers):
        usernames = []
        emails = []
        for item in receivers:
            item = item.strip()
            if item.startswith('@'):
                usernames.append(item.strip('@'))
            else:
                try:
                    validate_email(item)
                    emails.append(item)
                except ValidationError:
                    continue
        return usernames, emails
    
        
    @action(detail=True, methods=['POST',],
            url_path='discourage', url_name='loan-officer-realtor-discourage')
    def discourage(self, request, *args, **kwargs):
        realtor = self.get_object()
        loan_officer = self.request.user.loan_officer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        discourage, created = Discourage.objects.update_or_create(
            discouraging_content_type=ContentType.objects.get_for_model(loan_officer),
            discouraging_object_id = loan_officer.id,
            discouraged_content_type=ContentType.objects.get_for_model(realtor),
            discouraged_object_id = realtor.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails,
                'comments' : request.data.get('comments', '')
            })
        discourage.users_discouraged_to.add(*list(HomeCaptainUser.objects.\
                                                  filter(username__in=usernames)))
        self.logger.info('Successfully discouraged Realtor ' + realtor.user.username)
        return Response({
            'discourage_count': Discourage.objects.filter(
                discouraged_content_type=ContentType.objects.get_for_model(realtor),
                discouraged_object_id = realtor.id).count(),
            'message': 'Successfully discouraged the Realtor'
        })


    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='loan-officer-realtor-recommend')
    def recommend(self, request, *args, **kwargs):
        realtor = self.get_object()
        loan_officer = self.request.user.loan_officer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(loan_officer),
            recommending_object_id = loan_officer.id,
            recommended_content_type=ContentType.objects.get_for_model(realtor),
            recommended_object_id = realtor.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails,
                'comments' : request.data.get('comments', '')
            })
        recommend.users_recommended_to.add(*list(HomeCaptainUser.objects.\
                                                 filter(username__in=usernames)))
        self.logger.info('Successfully recommended Realtor ' + realtor.user.username)
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(realtor),
                recommended_object_id = realtor.id).count(),
            'message': 'Successfully recommend the Realtor'
        })
    
    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='loan-officer-realtor-archive')
    def archive(self, request, *args, **kwargs):
        realtor = self.get_object()
        loan_officer = self.request.user.loan_officer
        loan_officer.add_realtor_to_archive(realtor.id)
        loan_officer.save()
        self.logger.info('Archived Realtor ' + realtor.user.username)
        return Response({'message': 'Archived realtor %s' % \
                         realtor.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='loan-officer-realtor-unarchive')
    def restore(self, request, *args, **kwargs):
        ##FIXME: change to restore @brenton and let @kan101 know
        realtor = self.get_object()
        loan_officer = self.request.user.loan_officer
        loan_officer.remove_realtor_from_archive(realtor.id)
        loan_officer.save()
        self.logger.info('Restored Realtor ' + realtor.user.username)
        return Response({'message': 'Restored realtor %s' % \
                         realtor.user.username})
