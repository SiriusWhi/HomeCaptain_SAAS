from collections import OrderedDict
from datetime import datetime
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status , generics , mixins
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import (
    action,
    api_view,
    detail_route,
    list_route
)
from django_filters import rest_framework as filters

from django.contrib.postgres.search import SearchVector
from django.db.models import Count, Q, Min, Max
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from apps.util.permissions import IsOwnerOrReadOnly, IsRealtor
from apps.util.utils import create_export_xlsx, get_usernames_and_emails
from apps.hcauth.models import Discourage, Recommend, Archive
from apps.customer.models import Customer, CustomerUpdate
from apps.customer.serializers import CustomerSerializer, CustomerRealtorUpdateSerializer
from apps.hcauth.models import HomeCaptainRecommend, HomeCaptainUser
from apps.property.serializers import PropertyRealtorOrLoanOfficerUpdateSerializer
from apps.property.models import Property
from apps.requirement.models import Requirement
from .models import Realtor
from .serializers import RealtorOnlySerializer, RealtorPortalSerializer
from apps.util.picklists import (BUYER_MILESTONES_CHOICES, BUYER_MILESTONES_CHOICES_DICTS,
                                 SELLER_MILESTONES_CHOICES, SELLER_MILESTONES_CHOICES_DICTS,
                                 MILESTONES_CHOICES, EVENT_CHOICES)
from apps.lender.serializers import LoanOfficerSerializer
from apps.lender.models import LoanOfficer
from apps.event.serializers import EventSerializer
from apps.event.models import Event
from apps.concierge.serializers import ConciergeSerializer
from apps.concierge.models import Concierge


class RealtorSelfProfileViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Realtor.objects.all()
    serializer_class = RealtorPortalSerializer
    logger = logging.getLogger('RealtorSelfProfileViewSet')
    
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and 
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        realtor = request.user.realtor
        serializer = self.get_serializer(realtor)
        return Response(serializer.data)

    def update(self, request):
        realtor = request.user.realtor
        serializer = self.get_serializer(realtor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        self.logger.info(str(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        realtor = request.user.realtor
        serializer = self.get_serializer(realtor, data=request.data, partial=True)
        if serializer.is_valid():
            print("DATA")
            serializer.save()
            return Response(serializer.data)
        self.logger.info(str(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RealtorDashboardCustomersViewSet(mixins.ListModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.RetrieveModelMixin,
                                        viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsRealtor)
    serializer_class = CustomerRealtorUpdateSerializer
    queryset = Customer.objects.all()
    filter_fields = ('milestones', )
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('RealtorDashboardCustomersViewSet')

    DASHBOARD_PAGE = 'dashboard'
    BUYING_PAGE = 'buying'
    SELLING_PAGE = 'selling'
    PAGE = None
    
    BUYER = "Buyer"
    SELLER = "Seller"
    BOTH = "Both"
    
    def get_queryset(self):
        self.PAGE = self.request.data.get('page', '') or self.request.GET.get('page', '')
        seller = self.request.GET.get('seller', '') or self.PAGE == self.SELLING_PAGE
        search = self.request.GET.get('search', '') 
        buyer = self.request.GET.get('buyer', '') or self.PAGE == self.BUYING_PAGE
        needs_update = self.request.GET.get('needs_update', '')
        queryset = self.queryset

        if buyer:
            queryset = queryset.filter(
                requirements__realtor__user=self.request.user,
                buyer_seller__in=['Buyer', 'Both'])
        elif seller:
            queryset = queryset.filter(
                properties__realtor__user=self.request.user,
                buyer_seller__in=['Seller', 'Both'])
        elif needs_update:
            queryset = self.add_needs_update_filters(
                queryset.filter(
                    Q(properties__realtor__user=self.request.user)|
                    Q(requirements__realtor__user=self.request.user)
                )
            )
        else:
            queryset = queryset.filter(
                Q(properties__realtor__user=self.request.user)|
                Q(requirements__realtor__user=self.request.user))
        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name'),
            ).filter(search__icontains=search).filter(requirements__realtor__user=self.request.user)
        if self.request.GET.get('milestones', '') != 'Archived' and self.action != 'restore':
            queryset = queryset.exclude(milestones='Archived')
        return queryset.distinct()

    def add_needs_update_filters(self, queryset):
        return queryset.filter(update_history__is_updated=False)

    @action(detail=True, methods=['PATCH',],
            url_path='status-update', url_name='realtor-customer-status-update')
    def status_update(self, request, *args, **kwargs):
        if not self.request.data.get('milestones', None):
            raise Exception("'milestones', this field is required")
        customer = self.get_object()
        customer.close_update_request(self.request.data['milestones'], user=self.request.user)
        return Response({
            "milestones": self.request.data['milestones']
        })

    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='realtor-dashboard-customer-stats')
    def stats(self, request, *args, **kwargs):
        qs = self.get_queryset()
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
        stats = list(qs.values('milestones').annotate(Count('milestones')))
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
        counts_qs = self.queryset.filter(
            Q(properties__realtor__user=self.request.user)|
            Q(requirements__realtor__user=self.request.user)
        )
        result['filters'] = stats
        if self.PAGE == self.DASHBOARD_PAGE:
            result['counts'] = {
                'buyers': counts_qs.filter(buyer_seller__in=[self.BUYER, self.BOTH]).count(),
                'sellers': counts_qs.filter(buyer_seller__in=[self.SELLER, self.BOTH]).count(),
                'all': counts_qs.distinct().count(),
                'needs_update': self.add_needs_update_filters(counts_qs).count()
            }
        return Response(result)

    @action(detail=False, methods=['GET',],
            url_path='export-customers',
            url_name='realtor-customer-export-customers')
    def export_customers(self, request):
        #removed json body in GET in favor of REST guidelines
        #https://stackoverflow.com/questions/978061/http-get-with-request-body
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
                report_name = "Realtor-Sellers-Export"
            else:
                report_name = "Realtor-Buyers-Export"
            self.logger.info('Exporting ' + report_name)
            return create_export_xlsx(report_name, headers, customers_data)
        return Response({
            "detail": "Send GET request with query param `uids`, with values separate by commas. `uid` is `customer.uid`",
        })

    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='realtor-home-customer-archive')
    def archive(self, request, *args, **kwargs):
        customer = self.get_object()
        realtor = self.request.user.realtor
        customer.milestones = 'Archived'
        customer.save()

        if customer.buyer_seller == 'Buyer' or customer.buyer_seller == 'Both':
            for requirement in customer.requirements.all():
                realtor.add_requirement_to_archive(requirement.id)
        
        if customer.buyer_seller == 'Seller' or customer.buyer_seller == 'Both':
            for prop in customer.properties.all():
                realtor.add_property_to_archive(prop.id)
        self.logger.info('Archived buyer %s' % customer.user.username)
        return Response({'message': 'Archived buyer %s' % customer.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='realtor-home-customer-restore')
    def restore(self, request, *args, **kwargs):
        customer = self.get_object()
        realtor = self.request.user.realtor
        customer.milestones = 'Searching Reset'
        customer.save()

        if customer.buyer_seller == 'Buyer' or customer.buyer_seller == 'Both':
            for requirement in customer.requirements.all():
                realtor.remove_requirement_from_archive(requirement.id)
        
        if customer.buyer_seller == 'Seller' or customer.buyer_seller == 'Both':
            for prop in customer.properties.all():
                realtor.remove_property_from_archive(prop.id)
        self.logger.info('Restored customer %s' % customer.user.username)
        return Response({'message': 'Restored customer %s' % customer.user.username})


class PropertyFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="target_price_minimum", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="target_price_maximum", lookup_expr='lte')
    min_sqft = filters.NumberFilter(field_name="square_feet", lookup_expr='gte')
    max_sqft = filters.NumberFilter(field_name="square_feet", lookup_expr='lte')
    location = filters.CharFilter(field_name="address__city", lookup_expr='iexact')
    
    class Meta:
        model = Property
        fields = [
            'location', 'min_price', 'max_price', 'min_sqft', 'max_sqft',
            'bedrooms', 'bathrooms'
        ]
                                    
    
class RealtorPropertiesViewSet(mixins.ListModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsRealtor, )
    serializer_class = PropertyRealtorOrLoanOfficerUpdateSerializer
    queryset = Property.objects.all()
    filterset_class = PropertyFilter
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('RealtorPropertiesViewSet')

    def get_queryset(self, *args, **kwargs):
        queryset = Property.objects.filter()
        search = self.request.GET.get('search', None) 
        favorites = self.request.GET.get('favorites', False) or kwargs.get('favorites', None) or \
                    self.request.GET.get('favorite', False) or kwargs.get('favorite', None)
        recommended = self.request.GET.get('recommended', None) or kwargs.get('recommended', None)
        search_client = self.request.GET.get('search_client', None)
        realtor = self.request.user.realtor
        
        if self.action == 'archived':
            return queryset.filter(id__in=realtor.archived_properties.\
                                        values_list('archived_object_id', flat=True))

        if favorites:
            #logic: only properties that are favorited or reqeusted appointments by their buyers
            #we don't have appointments yet, so only favorited by buyers assocaited with realtor
            favorite_property_ids = realtor.requirement_set.\
                                    values_list('customer__user__favorite_property__id', \
                                                flat=True)
            queryset = queryset.filter(id__in=favorite_property_ids).order_by('-favorite_count')
            if self.request.GET.get('has_showings', None):
                queryset = self._get_has_showings_queryset(queryset)
        elif not recommended:
            #logic: only properties that are favorited or reqeusted appointments by their buyers
            #we don't have appointments yet, so only favorited by buyers assocaited with realtor
            #and posted by their sellers are selling
            ##Note: can be optimized using values_list, with flat=true flag
            realtor_buyer_ids = realtor.requirement_set.values_list('customer__user__id', flat=True)
            seller_user_ids = realtor.property_set.values_list('customer__user__id', flat=True)
            #favorite_user_ids = realtor.requirement_set.values_list('customer__user__id', flat=True)
            queryset = queryset.filter(\
                                       Q(favorite_users__id__in=realtor_buyer_ids)|\
                                       Q(customer__user__id__in=seller_user_ids)|\
                                       Q(events__buyer__id__in=realtor_buyer_ids)|\
                                       Q(events__requested_by__id__in=realtor_buyer_ids)|\
                                       Q(events__requested_by__id=self.request.user.id)\
            ).\
            distinct().order_by('-favorite_count')
                
        if search:
            queryset = queryset.annotate(
                search=SearchVector('description',),
            ).filter(search__icontains=search)
        
        if search_client:
            queryset = queryset.filter(customer__user__first_name__icontains=search_client)

        if self.action != 'restore':
            queryset = queryset.exclude(id__in=realtor.archived_properties.\
                                        values_list('archived_object_id', flat=True))

        ##Note: slicing should happen at the last
        if favorites and self.request.GET.get('top', None):
            queryset = queryset[:10]

        return queryset

    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='realtor-listings-archived')
    def archived(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
  
    @action(detail=False, methods=['GET',],
            url_path='filters', url_name='realtor-listings-filters')
    def get_facets(self, request, *args, **kwargs):
        queryset = self.filterset_class(data=request.GET,
                                        queryset=self.get_queryset(),
                                        request=request).qs
        cities = [i['address__city'] for i in queryset.values('address__city')\
                  .annotate(Count('address__city'))]

        res = self.normalize_filters(
            queryset.aggregate(
                min_price=Min('target_price_minimum'), max_price=Max('target_price_maximum'),
                min_sqft=Min('square_feet'), max_sqft=Max('square_feet'),
                min_bathrooms=Min('bathrooms'), max_bathrooms=Max('bathrooms'),
                min_bedrooms=Min('bedrooms'), max_bedrooms=Max('bedrooms')
            ))
        res['cities'] = cities
        return Response(res)

    def _get_has_showings_queryset(self, queryset):
        return queryset.filter(events__proposed_start__gt=datetime.now()).distinct()
    
    @action(detail=False, methods=['GET',],
            url_path='favorite-filters', url_name='realtor-listings-favorite-filters')
    def get_fav_facets(self, request, *args, **kwargs):
        queryset = self.get_queryset(favorites=1)
        filters = {
            'has_showings': self._get_has_showings_queryset(
                self.get_queryset(favorites=1)).count(),
            'total_favorites': self.get_queryset(favorites=1).count()
        }
        return Response(filters)
    
    def normalize_filters(self, filters):
                
        price_range_min_int = filters.get('min_price', 0) or 0
        price_range_min_int = int(price_range_min_int / 100000)
        price_range_max_int = filters.get('max_price', 0) or 0
        price_range_max_int = int(price_range_max_int / 100000)
        filters['price_range'] = []
        for i in range(price_range_min_int, price_range_max_int + 1):
            filters['price_range'].append((i*int(100000), i*int(100000) + int(100000)))
        
        area_range_minimum = filters.get('min_sqft', 0) or 0
        area_range_minimum = int(area_range_minimum / 1000)
        area_range_maximum = filters.get('max_sqft', 0) or 0
        area_range_maximum = int(area_range_maximum / 1000)
        filters['area_range'] = []
        for i in range(area_range_minimum, area_range_maximum + 1):
            filters['area_range'].append((i*1000, i*1000 + 1000))
                                 
        return filters
    
    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='realtor-listings-recommend')
    def recommend(self, request, *args, **kwargs):
        property = self.get_object()
        realtor = self.request.user.realtor
        usernames, emails = get_usernames_and_emails(self.request.data.get('receivers', []))
                
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(realtor),
            recommending_object_id = realtor.id,
            recommended_content_type=ContentType.objects.get_for_model(property),
            recommended_object_id = property.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails,
                'comments' : request.data.get('comments', '')
            })
        recommend.users_recommended_to.add(*list(HomeCaptainUser.objects.\
                                             filter(username__in=usernames)))
        self.logger.info('Successfully recommend property id %s' % property.id)                                             
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(property),
                recommended_object_id = property.id).count(),
            'message': 'Successfully recommend the property'
        })

    @action(detail=True, methods=['POST',],
            url_path='archive', url_name='realtor-property-archive')
    def archive(self, request, *args, **kwargs):
        realtor = self.request.user.realtor
        property = self.get_object()
        if property:
            realtor.add_property_to_archive(property.id)
            # Curently just archive associated seller assuming there is only one associated property for a seller
            # need to be changed in the future
            if property.customer:
                property.customer.milestones = 'Archived'
                property.save()
        self.logger.info('Archived property id %s' % property.id)
        return Response({'message': 'Archived property id %s' % property.id})

    @action(detail=True, methods=['POST',],
            url_path='restore', url_name='realtor-property-restore')
    def restore(self, request, *args, **kwargs):
        realtor = self.request.user.realtor
        property = self.get_object()
        if property:
            realtor.remove_property_from_archive(property.id)
            # Curently just restore associated seller assuming there is only one associated property for a seller
            # need to be changed in the future
            if property.customer:
                property.customer.milestones = 'Searching Reset'
                property.save()
        self.logger.info('Restored property id %s' % property.id)
        return Response({'message': 'Restored property id %s' % property.id})

    
class RealtorDashboardMyLoanOfficerViewSet(mixins.ListModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.RetrieveModelMixin,
                                           viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsRealtor)
    serializer_class = LoanOfficerSerializer
    queryset = LoanOfficer.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('RealtorDashboardMyLoanOfficerViewSet')
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        prior = self.request.GET.get('prior', '')
        realtor = self.request.user.realtor

        if self.action == 'archived':
            return self.queryset.filter(id__in=realtor.archived_loan_officers.\
                                        values_list('archived_object_id', flat=True))

        if prior:
            queryset = self.queryset.filter(id__in=realtor.archived_loan_officers.\
                                        values_list('archived_object_id', flat=True))
            return queryset
        else:
            queryset = self.queryset.filter(
                requirements__realtor__user=self.request.user).distinct()
            ##added distinct because there are same pairs of realtors
            ##and loan officers working on a requirement as well as properties
        
        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name'),
            ).filter(search__icontains=search)

        if self.action != 'restore':
            queryset = queryset.exclude(id__in=realtor.archived_loan_officers.\
                                        values_list('archived_object_id', flat=True))
        return queryset

    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='realtor-dashboard-loan-officer-archived')
    def archived(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) 

    def get_object(self):
        ##NOTE: HAD TO OVERRIDE THIS
        ##the filtered and difference'd queryset from get_object
        ##return's 2 objects for a given LO uid on a .get(uid=uid) call
        ##so used a get_object_or_404
        #print(self.kwargs['uid'])
        #print(self.get_queryset().filter(uid=self.kwargs['uid']).distinct())
        #return super(RealtorDashboardMyLoanOfficerViewSet, self).get_object()
        return get_object_or_404(LoanOfficer, uid=self.kwargs['uid'])

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        for lo in serializer.data:
            #FIXME: this a subpar way of changing the data dynamically
            #can we do this in serializer? or somewhere else?
            loan_officer = LoanOfficer.objects.get(id=lo['id'])
            lo.update({
                'realtor_users': loan_officer.get_realtor_customers(
                    request.user.realtor.id),
                #'recommend_count': loan_officer.recommendations_received.count(),
                #'discourage_count': loan_officer.discourages_received.count()
            })

        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)

        
        
    
    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='realtor-dashboard-loan-officer-stats')
    def stats(self, request, *args, **kwargs):
        return Response({
            'current_count': self.get_queryset().count(),
            'prior_count': self.request.user.realtor.\
            archived_loan_officers.count(),
            'buyers': request.user.realtor\
            .requirement_set.values_list('customer__user__username', flat=True)
        })

    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='realtor-loan-officer-recommend')
    def recommend(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        realtor = self.request.user.realtor
        usernames, emails = get_usernames_and_emails(self.request.data.get('receivers', []))
                
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(realtor),
            recommending_object_id = realtor.id,
            recommended_content_type=ContentType.objects.get_for_model(loan_officer),
            recommended_object_id = loan_officer.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails,
                'comments' : request.data.get('comments', '')
            })
        recommend.users_recommended_to.add(*list(HomeCaptainUser.objects.\
                                             filter(username__in=usernames)))
        self.logger.info('Successfully discouraged the Loan Officer %s' % loan_officer.user.username)
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(loan_officer),
                recommended_object_id = loan_officer.id).count(),
            'message': 'Successfully recommended the Loan Officer'
        })

    @action(detail=True, methods=['POST',],
            url_path='discourage', url_name='realtor-loan-officer-discourage')
    def discourage(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        realtor = self.request.user.realtor
        usernames, emails = get_usernames_and_emails(self.request.data.get('receivers', []))
        discourage, created = Discourage.objects.update_or_create(
            discouraging_content_type=ContentType.objects.get_for_model(realtor),
            discouraging_object_id = realtor.id,
            discouraged_content_type=ContentType.objects.get_for_model(loan_officer),
            discouraged_object_id = loan_officer.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails, 'comments' : request.data.get('comments', '')
            })
        discourage.users_discouraged_to.add(*list(HomeCaptainUser.objects.\
                                                  filter(username__in=usernames)))
        self.logger.info('Successfully discouraged the Loan Officer %s' % loan_officer.user.username)
        return Response({
            'discourage_count': Discourage.objects.filter(
                discouraged_content_type=ContentType.objects.get_for_model(loan_officer),
                discouraged_object_id = loan_officer.id).count(),
            'message': 'Successfully discouraged the Loan Officer'
        })

    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='realtor-loan-officer-archive')
    def archive(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        realtor = self.request.user.realtor
        realtor.add_loan_officer_to_archive(loan_officer.id)
        realtor.save()
        self.logger.info('Successfully archived the Loan Officer %s' % loan_officer.user.username)
        return Response({'message': 'Archived loan officer %s' % \
                         loan_officer.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='realtor-loan-officer-restore')
    def restore(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        realtor = self.request.user.realtor
        realtor.remove_loan_officer_from_archive(loan_officer.id)
        realtor.save()
        self.logger.info('Successfully restored the Loan Officer %s' % loan_officer.user.username)
        return Response({'message': 'Restored loan officer %s' % \
                         loan_officer.user.username})
    
    
class RealtorDashboardEventSlotViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsRealtor)
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('RealtorDashboardEventSlotViewSet')

    def get_queryset(self):
        queryset = self.queryset.filter(
            Q(requested_by=self.request.user)|
            Q(additional_attendees__in=[self.request.user,])|
            Q(property__realtor__user=self.request.user)).distinct()
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
        if request_data.get('buyer', None):
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
            self.logger.info(str(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        request_data = self.augment_request_data(request.data)
        serializer = self.get_serializer(self.get_object(), data = request_data)
        if serializer.is_valid(): #raise_exception=True):
            self.perform_update(serializer)
            serializer_data = self.augment_serializer_data(serializer.data)
            return Response(serializer_data, status=status.HTTP_201_CREATED)
        else:
            self.logger.info(str(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['GET',],
            url_path='extras', url_name='realtor-dashboard-agenda-extras')
    def extras(self, request, *args, **kwargs):
        return Response({
            'event_names': [e[0] for e in EVENT_CHOICES],
            'buyers': request.user.realtor\
            .requirement_set.values_list('customer__user__username', flat=True),
            'addresss': request.user.realtor\
            .property_set.values_list('address__street', 'id')
        })


class RealtorDashboardMyConciergeViewSet(mixins.ListModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.RetrieveModelMixin,
                                           viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsRealtor)
    serializer_class = ConciergeSerializer
    queryset = Concierge.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('RealtorDashboardMyConciergeViewSet')

    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        prior = self.request.GET.get('prior', '')
        realtor = self.request.user.realtor

        if self.action == 'archived':
            return self.queryset.filter(id__in=realtor.archived_concierges.\
                                        values_list('archived_object_id', flat=True))
        if prior:
            queryset = self.queryset.filter(id__in=realtor.archived_concierges.\
                                        values_list('archived_object_id', flat=True))
            return queryset
        else:
            queryset = self.queryset.filter(
                requirement__realtor__user=self.request.user).distinct()
            ##added distinct because there are same pairs of realtors
            ##and concierges working on a requirement as well as properties

        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name'),
            ).filter(search__icontains=search)

        if self.action != 'restore':
            queryset = queryset.exclude(id__in=realtor.archived_concierges.\
                                        values_list('archived_object_id', flat=True))        
    
        return queryset

    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='realtor-concierge-archived')
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
                'realtor_users': concierge.get_realtor_customers(request.user.realtor.id)
            })

        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)

    def get_object(self):
        ##NOTE: HAD TO OVERRIDE THIS
        ##the filtered and difference'd queryset from get_object
        ##return's 2 objects for a given LO uid on a .get(uid=uid) call
        ##so used a get_object_or_404
        #print(self.kwargs['uid'])
        #print(self.get_queryset().filter(uid=self.kwargs['uid']).distinct())
        #return super(RealtorDashboardMyLoanOfficerViewSet, self).get_object()
        return get_object_or_404(Concierge, uid=self.kwargs['uid'])    
    
    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='realtor-concierge-stats')
    def stats(self, request, *args, **kwargs):
        return Response({
            'current': self.get_queryset().count(),
            'prior_count': self.request.user.realtor.\
            archived_concierges.count(),
            'buyers': request.user.realtor\
            .requirement_set.values_list('customer__user__username', flat=True)
        })


    @action(detail=True, methods=['POST',],
            url_path='discourage', url_name='realtor-concierge-discourage')
    def discourage(self, request, *args, **kwargs):
        concierge = self.get_object()
        realtor = self.request.user.realtor
        usernames = []
        emails = []
        for item in self.request.data.get('receivers', []):
            item = item.strip()
            if item.startswith('@'):
                usernames.append(item.strip('@'))
            else:
                try:
                    validate_email(item)
                    emails.append(item)
                except ValidationError:
                    continue

        discourage, created = Discourage.objects.update_or_create(
            discouraging_content_type=ContentType.objects.get_for_model(realtor),
            discouraging_object_id = realtor.id,
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
            url_path='recommend', url_name='realtor-concierge-recommend')
    def recommend(self, request, *args, **kwargs):
        concierge = self.get_object()
        realtor = self.request.user.realtor
        usernames = []
        emails = []
        for item in self.request.data.get('receivers', []):
            item = item.strip()
            if item.startswith('@'):
                usernames.append(item.strip('@'))
            else:
                try:
                    validate_email(item)
                    emails.append(item)
                except ValidationError:
                    continue
                
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(realtor),
            recommending_object_id = realtor.id,
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
        self.logger.info('Successfully recommended the Concierge ' + concierge.user.username)
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(concierge),
                recommended_object_id = concierge.id).count(),
            'message': 'Successfully recommend the concierge'
        })

    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='realtor-concierge-archive')
    def archive(self, request, *args, **kwargs):
        concierge = self.get_object()
        realtor = self.request.user.realtor
        realtor.add_concierge_to_archive(concierge.id)
        realtor.save()
        self.logger.info('Archived concierge %s'  % concierge.user.username)
        return Response({'message': 'Archived concierge %s' % \
                         concierge.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='realtor-concierge-unarchive')
    def restore(self, request, *args, **kwargs):
        ##FIXME: change to restore @brenton and let @kan101 know
        concierge = self.get_object()
        realtor = self.request.user.realtor
        realtor.remove_concierge_from_archive(concierge.id)
        realtor.save()
        self.logger.info('Restored concierge %s'  % concierge.user.username)
        return Response({'message': 'Restored concierge %s' % \
                         concierge.user.username})


class RealtorDashboardArchivedViewSet(viewsets.ViewSet):
    logger = logging.getLogger('RealtorDashboardArchivedViewSet')
    permission_classes = (permissions.IsAuthenticated, IsRealtor, )

    def list(self, request):

        ##FIXME: I think this needs a complete overhaul with the new archive process
        ##@brenton
        realtor = request.user.realtor
        queryset = Customer.objects.filter(
            requirements__realtor__user=self.request.user,
            buyer_seller__in=['Buyer', 'Both'],
            milestones='Archived')

        serializer = CustomerRealtorUpdateSerializer(queryset, many=True)
        archived_buyers = serializer.data

        queryset = Customer.objects.filter(
            properties__realtor__user=self.request.user,
            buyer_seller__in=['Seller', 'Both'],
            milestones='Archived')
        serializer = CustomerRealtorUpdateSerializer(queryset, many=True)
        archived_sellers = serializer.data

        favorite_users = [rq.customer.user for rq in realtor.requirement_set.all()]
        seller_user_uids = [p.customer.user.uid for p in realtor.property_set.all()]
        queryset = Property.objects.filter(Q(favorite_users__in=favorite_users)|
                                           Q(customer__user__uid__in=seller_user_uids),
                                           archived=True).\
                                           distinct().order_by('-favorite_count')
        serializer = PropertyRealtorOrLoanOfficerUpdateSerializer(queryset, many=True)
        archived_properties = serializer.data

        queryset = realtor.archived_loan_officers.all()
        serializer = LoanOfficerSerializer(queryset, many=True)
        archived_loan_officers = serializer.data

        queryset = realtor.archived_concierges.all()
        serializer = ConciergeSerializer(queryset, many=True)
        archived_concierges = serializer.data

        return Response(archived_buyers + archived_sellers + archived_properties + archived_loan_officers + archived_concierges)
