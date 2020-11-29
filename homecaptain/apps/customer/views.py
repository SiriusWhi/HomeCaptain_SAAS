import logging
from django.conf import settings
from datetime import datetime
from rest_framework import (
    status,
    generics,
    mixins,
    permissions,
    viewsets,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView
from django.db.models import F, Avg

from apps.concierge.models import Concierge
from apps.concierge.serializers import ConciergeSerializer
from apps.customer.models import Customer
from apps.hcauth.models import HomeCaptainUser, Recommend, Discourage, Archive
from apps.util.permissions import IsCustomer
from apps.util.tasks import generic_send_raw_email
from apps.util.utils import get_usernames_and_emails
from apps.util.picklists import EVENT_CHOICES
from apps.lender.models import LoanOfficer
from apps.lender.serializers import LoanOfficerSerializer
from apps.event.serializers import EventSerializer
from apps.event.models import Event
from apps.realtor.models import Realtor
from apps.realtor.serializers import RealtorSerializer, RealtorUserSerializer
from apps.requirement.models import Requirement
from apps.property.serializers import PropertyRealtorOrLoanOfficerUpdateSerializer
from apps.property.serializers import PropertySerializer
from apps.property.models import Property
from apps.util.models import Address
from apps.util.utils import getParsedLocation

from django.db.models import Count, Q, Min, Max
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector
from .models import CustomerUpdate
from .serializers import CustomerHomeCalculatorSerializer, CustomerHomeCalculatorAddPropertySerializer
from .serializers import CustomerMortgageCalculatorSerializer, CustomerPortalSerializer

# Create your views here.
class CustomerMyRealtorViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsCustomer)
    serializer_class = RealtorSerializer
    queryset = Realtor.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('CustomerMyRealtorViewSet')
    
    def get_queryset(self):
        customer = self.request.user.customer
        search = self.request.GET.get('search', '')
        prior = self.request.GET.get('prior', '')

        if self.action == 'all':
            queryset = self.queryset                                                        
        elif self.action == 'archived':
            queryset = self.queryset.filter(id__in=customer.archived_realtors.\
                                        values_list('archived_object_id', flat=True))
        else:
            if prior:
                queryset = self.queryset.filter(id__in=customer.archived_realtors.\
                                            values_list('archived_object_id', flat=True))
            else:
                queryset = (self.queryset.filter(
                    requirement__customer__user=self.request.user
                ).distinct() | self.queryset.filter(
                    property__customer__user=self.request.user
                ).distinct()).distinct()
                    
            if self.action != 'restore':
                queryset = queryset.exclude(id__in=customer.archived_realtors.\
                                            values_list('archived_object_id', flat=True))     

        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name', 'broker__company'),
            ).filter(search__icontains=search)

        return queryset.distinct()


    def get_object(self):
        ##NOTE: HAD TO OVERRIDE THIS
        ##the filtered and difference'd queryset from get_object
        ##return's 2 objects for a given LO uid on a .get(uid=uid) call
        ##so used a get_object_or_404
        return get_object_or_404(Realtor, uid=self.kwargs['uid'])

    @action(detail=False, methods=['POST',],
            url_path='request', url_name='customer-request-realtor')
    def request(self, request, *args, **kwargs):
        customer = self.request.user.customer
        customer_update = CustomerUpdate()
        customer_update.request_type = 'Realtor Requested'
        customer_update.customer = customer
        
        if customer.buyer_seller == 'Buyer':
            customer_update.requirement = customer.requirements.first()
        else:
            property = customer.properties.first()
            customer_update.property = property

        customer_update.requested_by = self.request.user
        customer_update.save()
        self.logger.info("Successfully requested a relator")
        return Response({
            "message": "Successfully requested a relator"
        })

    @action(detail=False, methods=['POST',],
            url_path='send_invite', url_name='customer-send-invite-realtor')
    def send_invite(self, request, *args, **kwargs):
        customer = self.request.user.customer
        message = request.data.pop('message')
        user = request.data.get('user', None)
        if user is None:
            return HttpResponseBadRequest("user data is required")

        email = user.get('email', None)
        if email is None:
            return Response(
                {
                    "message": "email is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        realtor_serializer = RealtorUserSerializer(data=request.data, context={'request': request})
        if not realtor_serializer.is_valid():
            self.logger.info("invalid user data")
            return Response(
                {
                    "message": "invalid user data"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        realtor_serializer.save()

        generic_send_raw_email.delay(request.user.uid,
                                     email, "Realtor Invitation", message, 'invite-realtor')
        self.logger.info("Successfully sent invitation")
        return Response({
            "message": "Successfully sent invitation"
        })                

    @action(detail=False, methods=['POST',],
            url_path='assign', url_name='customer-assign-realtor')
    def assign(self, request, *args, **kwargs):
        customer = self.request.user.customer
        realtor_uid = request.data.get('realtor_uid', None)
        realtor = get_object_or_404(Realtor, uid=realtor_uid)
        
        if customer.buyer_seller == 'Buyer':
            requirement = customer.requirements.first()
            if requirement is None:
                requirement = Requirement()
                requirement.customer = customer
            if requirement.realtor:
                return Response(
                    {
                        "message": "Realtor already assigned"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            requirement.realtor = realtor
            requirement.save()
        else:
            property = customer.properties.first()
            if property.realtor:
                return Response(
                    {
                        "message": "Realtor already assigned"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            property.realtor = realtor
            property.save()

        self.logger.info("Assignd the realtor id %s to the customer id %s" % (realtor.id, customer.id))
        return Response({
            "message": "Assignd the realtor to the customer"
        })       
    
    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='customer-realtor-stats')
    def stats(self, request, *args, **kwargs):
        return Response({
            'current': self.get_queryset().count(),
            'prior_count': self.request.user.customer.\
            archived_realtors.count(),
        })
    
    @action(detail=False, methods=['GET',],
            url_path='all', url_name='customer-realtor-all')
    def all(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='customer-realtor-archived')
    def archived(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
            url_path='discourage', url_name='customer-realtor-discourage')
    def discourage(self, request, *args, **kwargs):
        realtor = self.get_object()
        customer = self.request.user.customer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        discourage, created = Discourage.objects.update_or_create(
            discouraging_content_type=ContentType.objects.get_for_model(customer),
            discouraging_object_id = customer.id,
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
        self.logger.info('Successfully discouraged the Realtor id %s' % realtor.id)
        return Response({
            'discourage_count': Discourage.objects.filter(
                discouraged_content_type=ContentType.objects.get_for_model(realtor),
                discouraged_object_id = realtor.id).count(),
            'message': 'Successfully discouraged the Realtor'
        })


    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='customer-realtor-recommend')
    def recommend(self, request, *args, **kwargs):
        realtor = self.get_object()
        customer = self.request.user.customer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(customer),
            recommending_object_id = customer.id,
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
        self.logger.info('Successfully recommended the Realtor id %s' % realtor.id)
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
        customer = self.request.user.customer
        customer.add_realtor_to_archive(realtor.id)
        customer.save()
        self.logger.info('Archived the Realtor id %s' % realtor.id)
        return Response({'message': 'Archived realtor %s' % \
                         realtor.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='loan-officer-realtor-unarchive')
    def restore(self, request, *args, **kwargs):
        ##FIXME: change to restore @brenton and let @kan101 know
        realtor = self.get_object()
        customer = self.request.user.customer
        customer.remove_realtor_from_archive(realtor.id)
        customer.save()
        self.logger.info('Restored the Realtor id %s' % realtor.id)
        return Response({'message': 'Restored realtor %s' % \
                         realtor.user.username})

class CustomerMyConciergeViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsCustomer)
    serializer_class = ConciergeSerializer
    queryset = Concierge.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('CustomerMyConciergeViewSet')
    
    def get_queryset(self):
        customer = self.request.user.customer
        search = self.request.GET.get('search', '')
        prior = self.request.GET.get('prior', '')
        if self.action == 'archived':
            return self.queryset.filter(id__in=customer.archived_concierges.\
                                        values_list('archived_object_id', flat=True))
        if prior:
            queryset = self.queryset.filter(id__in=customer.archived_concierges.\
                                        values_list('archived_object_id', flat=True))
            return queryset
        else:
            queryset = (self.queryset.filter(
                requirement__customer__user=self.request.user) | \
                self.queryset.filter(property__customer__user=self.request.user)).distinct()
        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name'),
            ).filter(search__icontains=search)

        if self.action != 'restore':
            queryset = queryset.exclude(id__in=customer.archived_concierges.\
                                        values_list('archived_object_id', flat=True))     
        return queryset.distinct()


    def get_object(self):
        ##NOTE: HAD TO OVERRIDE THIS
        ##the filtered and difference'd queryset from get_object
        ##return's 2 objects for a given LO uid on a .get(uid=uid) call
        ##so used a get_object_or_404
        return get_object_or_404(Concierge, uid=self.kwargs['uid'])    
    
    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='customer-concierge-stats')
    def stats(self, request, *args, **kwargs):
        return Response({
            'current': self.get_queryset().count(),
            'prior_count': self.request.user.customer.\
            archived_concierges.count(),
        })
    
    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='customer-concierge-archived')
    def archived(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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
            url_path='discourage', url_name='customer-concierge-discourage')
    def discourage(self, request, *args, **kwargs):
        concierge = self.get_object()
        customer = self.request.user.customer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        discourage, created = Discourage.objects.update_or_create(
            discouraging_content_type=ContentType.objects.get_for_model(customer),
            discouraging_object_id = customer.id,
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
        self.logger.info('Successfully discouraged the Concierge Id %s' % concierge.id)
        return Response({
            'discourage_count': Discourage.objects.filter(
                discouraged_content_type=ContentType.objects.get_for_model(concierge),
                discouraged_object_id = concierge.id).count(),
            'message': 'Successfully discouraged the Concierge'
        })


    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='customer-concierge-recommend')
    def recommend(self, request, *args, **kwargs):
        concierge = self.get_object()
        customer = self.request.user.customer
        usernames, emails = self._recommend_discourage_dry(self.request.data.get('receivers', []))
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(customer),
            recommending_object_id = customer.id,
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
        self.logger.info('Successfully recommended the Concierge Id %s' % concierge.id)
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(concierge),
                recommended_object_id = concierge.id).count(),
            'message': 'Successfully recommend the Concierge'
        })
    
    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='customer-concierge-archive')
    def archive(self, request, *args, **kwargs):
        concierge = self.get_object()
        customer = self.request.user.customer
        customer.add_concierge_to_archive(concierge.id)
        customer.save()
        self.logger.info('Successfully archived the Concierge Id %s' % concierge.id)
        return Response({'message': 'Archived concierge %s' % \
                         concierge.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='customer-concierge-unarchive')
    def restore(self, request, *args, **kwargs):
        ##FIXME: change to restore @brenton and let @kan101 know
        concierge = self.get_object()
        customer = self.request.user.customer
        customer.remove_concierge_from_archive(concierge.id)
        customer.save()
        self.logger.info('Successfully restored the Concierge Id %s' % concierge.id)
        return Response({'message': 'Restored concierge %s' % \
                         concierge.user.username})

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

class CustomerPropertyViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsCustomer)
    serializer_class = PropertyRealtorOrLoanOfficerUpdateSerializer
    queryset = Property.objects.all()
    filterset_class = PropertyFilter
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('CustomerPropertyViewSet')

    def get_queryset(self, *args, **kwargs):
        customer = self.request.user.customer
        search = self.request.GET.get('search', '')
        favorites = self.request.GET.get('favorites', False) or kwargs.get('favorites', None)
        recommended = self.request.GET.get('recommended', False) or kwargs.get('recommended', None)
        property_content_type = ContentType.objects.get_for_model(Property)
        queryset = self.queryset

        if favorites:
            favorited_ids = customer.get_favorited_ids(property_content_type)
            related_queryset = self.queryset.filter(customer=customer).order_by('-favorite_count')
            queryset = self.queryset.filter(id__in=favorited_ids).exclude(customer=customer) \
                .order_by('-favorite_count')
            return related_queryset | queryset

        if recommended:
            recommended_ids = Recommend.objects.filter(
                recommended_content_type=property_content_type,
                users_recommended_to=self.request.user,
            ).values_list('recommended_object_id')
            queryset = queryset.filter(id__in=recommended_ids)

        if search:
            queryset = queryset.annotate(
                search=SearchVector('description'),
            ).filter(search__icontains=search)
    
        return queryset.order_by('-favorite_count')

    # @action(detail=False, methods=['GET',],
    #         url_path='archived', url_name='customer-property-archived')
    # def archived(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

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

    @action(detail=False, methods=['GET',],
            url_path='filters', url_name='customer-listings-filters')
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
            url_path='favorite-filters', url_name='customer-listings-favorite-filters')
    def get_fav_facets(self, request, *args, **kwargs):
        filters = {
            'has_showings': self._get_has_showings_queryset(
                self.get_queryset(favorites=1)).count(),
            'total_favorites': self.get_queryset(favorites=1).count()
        }
        return Response(filters)

    def get_object(self):
        return get_object_or_404(Property, uid=self.kwargs['uid'])

    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='customer-property-recommend')
    def recommend(self, request, *args, **kwargs):
        property = self.get_object()
        customer = self.request.user.customer
        usernames, emails = get_usernames_and_emails(self.request.data.get('receivers', []))
                
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(customer),
            recommending_object_id = customer.id,
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
        self.logger.info("Successfully recommended property %s", property.uid)
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(property),
                recommended_object_id = property.id).count(),
            'message': 'Successfully recommended the property'
        })

    @action(detail=True, methods=['POST',],
            url_path='favorite', url_name='customer-property-favorite')
    def favorite(self, request, *args, **kwargs):
        property = self.get_object()
        customer = self.request.user.customer
        _, created = customer.favorite(ContentType.objects.get_for_model(property), property.id)
        if created == True:
            property.add_favorite_user(self.request.user)
        self.logger.info("Successfully favorited the property %s", property.uid)
        return Response({
            'favorite_count': property.favorite_count,
            'message': 'Successfuly favorited property'
        })

    @action(detail=True, methods=['POST',],
            url_path='unfavorite', url_name='customer-property-unfavorite')
    def unfavorite(self, request, *args, **kwargs):
        property = self.get_object()
        customer = self.request.user.customer
        is_unfavorited = customer.unfavorite(ContentType.objects.get_for_model(property), property.id)
        if is_unfavorited:
            property.remove_favorite_user(self.request.user)
        self.logger.info("Successfully unfavorited the property %s", property.uid)
        return Response({
            'favorite_count': property.favorite_count,
            'message': 'Successfuly unfavorited property'
        })               

    # @action(detail=True, methods=['POST',],
    #         url_path='archive',
    #         url_name='customer-property-archive')
    # def archive(self, request, *args, **kwargs):
    #     r_property = self.get_object()
    #     customer = self.request.user.customer
    #     customer.add_property_to_archive(r_property.id)
    #     customer.save()
    #     return Response({'message': 'Archived property %s' % \
    #                      r_property.address})
    # @action(detail=True, methods=['POST',],
    #         url_path='restore',
    #         url_name='customer-property-restore')
    # def restore(self, request, *args, **kwargs):
    #     r_property = self.get_object()
    #     customer = self.request.user.customer
    #     customer.remove_property_from_archive(r_property.id)
    #     customer.save()
    #     return Response({'message': 'Restored property  %s' % \
    #                      r_property.address})


class CustomerMyLoanOfficerViewSet(mixins.ListModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.RetrieveModelMixin,
                                           viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsCustomer)
    serializer_class = LoanOfficerSerializer
    queryset = LoanOfficer.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    logger = logging.getLogger('CustomerMyLoanOfficerViewSet')
    
    def get_queryset(self):
        customer = self.request.user.customer
        search = self.request.GET.get('search', '')
        prior = self.request.GET.get('prior', '')

        if self.action == 'all':
            queryset = self.queryset                                                        
        elif self.action == 'archived':
            queryset = self.queryset.filter(id__in=customer.archived_loan_officers.\
                                        values_list('archived_object_id', flat=True))
        else:
            if prior:
                queryset = self.queryset.filter(id__in=customer.archived_loan_officers.\
                                            values_list('archived_object_id', flat=True))
                return queryset
            else:
                queryset = self.queryset.filter(
                    requirements__customer__user=self.request.user
                ).distinct() 
                    
            if self.action != 'restore':
                queryset = queryset.exclude(id__in=customer.archived_loan_officers.\
                                            values_list('archived_object_id', flat=True))     

        if search:
            queryset = queryset.annotate(
                search=SearchVector('user__first_name', 'user__last_name', 'lender__name'),
            ).filter(search__icontains=search)

        return queryset.distinct()

    @action(detail=False, methods=['GET',],
            url_path='archived', url_name='customer-loan-officer-archived')
    def archived(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) 

    def get_object(self):
        return get_object_or_404(LoanOfficer, uid=self.kwargs['uid'])

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)

    @action(detail=False, methods=['GET',],
            url_path='all', url_name='customer-loan-officer-all')
    def all(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=['POST',],
            url_path='assign', url_name='customer-assign-loan-officer')
    def assign(self, request, *args, **kwargs):
        customer = self.request.user.customer
        loan_officer_uid = request.data.get('loan_officer_uid', None)
        loan_officer = get_object_or_404(LoanOfficer, uid=loan_officer_uid)
        
        if customer.buyer_seller == 'Buyer' or customer.buyer_seller == 'Both':
            requirement = customer.requirements.first()
            if requirement is None:
                requirement = Requirement()
                requirement.customer = customer
            if requirement.loan_officer:
                return Response(
                    data={
                        "message": "Loan Officer already assigned"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            requirement.loan_officer = loan_officer
            requirement.save()
        else:
            self.logger.info("Loan Officer should be assign to a buyer")
            return Response(
                data={
                    "message": "Loan Officer should be assign to a buyer"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.logger.info("Assigned the loan officer id %s to the customer %s" % (loan_officer.id, customer.id))
        return Response({
            "message": "Assignd the loan officer to the customer"
        })

    @action(detail=False, methods=['GET',],
            url_path='stats', url_name='customer-loan-officer-stats')
    def stats(self, request, *args, **kwargs):
        return Response({
            'current_count': self.get_queryset().count(),
            'prior_count': self.request.user.customer.\
            archived_loan_officers.count(),
        })

    @action(detail=True, methods=['POST',],
            url_path='recommend', url_name='customer-loan-officer-recommend')
    def recommend(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        customer = self.request.user.customer
        usernames, emails = get_usernames_and_emails(self.request.data.get('receivers', []))
                
        recommend, created = Recommend.objects.update_or_create(
            recommending_content_type=ContentType.objects.get_for_model(customer),
            recommending_object_id = customer.id,
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
        self.logger.info("Successfully recommended the loan officer id %s" % loan_officer.id)                                     
        return Response({
            'recommend_count': Recommend.objects.filter(
                recommended_content_type=ContentType.objects.get_for_model(loan_officer),
                recommended_object_id = loan_officer.id).count(),
            'message': 'Successfully recommended the Loan Officer'
        })

    @action(detail=True, methods=['POST',],
            url_path='discourage', url_name='customer-loan-officer-discourage')
    def discourage(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        customer = self.request.user.customer
        usernames, emails = get_usernames_and_emails(self.request.data.get('receivers', []))
        discourage, created = Discourage.objects.update_or_create(
            discouraging_content_type=ContentType.objects.get_for_model(customer),
            discouraging_object_id = customer.id,
            discouraged_content_type=ContentType.objects.get_for_model(loan_officer),
            discouraged_object_id = loan_officer.id,
            defaults = {
                'is_public' : request.data.get('is_public', None),
                'rating' : request.data.get('rating', None),
                'emails' : emails, 'comments' : request.data.get('comments', '')
            })
        discourage.users_discouraged_to.add(*list(HomeCaptainUser.objects.\
                                                  filter(username__in=usernames)))
        self.logger.info("Successfully discouraged the loan officer id %s" % loan_officer.id)
        return Response({
            'discourage_count': Discourage.objects.filter(
                discouraged_content_type=ContentType.objects.get_for_model(loan_officer),
                discouraged_object_id = loan_officer.id).count(),
            'message': 'Successfully discouraged the Loan Officer'
        })

    @action(detail=True, methods=['POST',],
            url_path='archive',
            url_name='customer-loan-officer-archive')
    def archive(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        customer = self.request.user.customer
        customer.add_loan_officer_to_archive(loan_officer.id)
        customer.save()
        self.logger.info("Archived the loan officer id %s" % loan_officer.id)
        return Response({'message': 'Archived loan officer %s' % \
                         loan_officer.user.username})

    @action(detail=True, methods=['POST',],
            url_path='restore',
            url_name='customer-loan-officer-restore')
    def restore(self, request, *args, **kwargs):
        loan_officer = self.get_object()
        customer = self.request.user.customer
        customer.remove_loan_officer_from_archive(loan_officer.id)
        customer.save()
        self.logger.info("Restored the loan officer id %s" % loan_officer.id)
        return Response({'message': 'Restored loan officer %s' % \
                         loan_officer.user.username})

class CustomerHomeCalculatorView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerHomeCalculatorSerializer
    def post(self, request, *args, **kwargs):
        serializer = CustomerHomeCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                parsedLocation = getParsedLocation(serializer.data['location'])
                address_components = parsedLocation['results'][0]['address_components']
                if 'city' in address_components.keys() and 'zip' in address_components.keys():
                    square_feet = int(serializer.data['square_feet'])
                    allowance = settings.SIMILAR_PROPERTY_SEARCH_SQUARE_FEET_ALLOWANCE
                    similar_properties = Property.objects.filter(
                        square_feet__gt=(square_feet-(allowance*square_feet)), \
                        square_feet__lt=(square_feet+(allowance*square_feet)), \
                        bedrooms=int(serializer.data['bedrooms']),
                        bathrooms=int(serializer.data['bathrooms']),
                        address__city__iexact=address_components['city'], \
                        address__postalcode=address_components['zip'])
                    
                    avg_psf = similar_properties.annotate(
                        avg_price=F('target_price_maximum')/F('square_feet')).\
                        aggregate(Avg('avg_price'))

                    if avg_psf['avg_price__avg'] is None:
                        return Response({'Info': 'No data to compare.'})
                    
                    similar_properties_list = []
                    for similar_property in similar_properties:
                        ##FIXME: this is a temporary solution to update the count
                        ##The actual fix will be to update prop fav cont using post_save signal on favorite a property methods
                        favorite_count = similar_property.get_favorite_count()
                        similar_properties_list.append({
                            'listing_title': similar_property.listing_title,
                            'listing_description': similar_property.listing_description,
                            'showing_count': similar_property.scheduled_showings['count'],
                            'favorite_count': favorite_count
                        })
                        
                    average = avg_psf['avg_price__avg']

                    data = {
                        'estimated_value': average * int(serializer.data['square_feet']),
                        'address_components': address_components,
                        'similar_properties': similar_properties_list 
                    }
                else:
                    return Response({'Error': 'Location needs City and Postal Code'})
            except Exception as e:
                 return Response({'Error': str(e)})
            return Response(data)
        else:
            return Response(serializer.errors)

class CustomerHomeCalculatorAddPropertyView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerHomeCalculatorAddPropertySerializer
    def post(self, request, *args, **kwargs):
        address = Address(
                unit_number=request.data['unit_number'],
                street=request.data['street'],
                state=request.data['state'],
                city=request.data['city'],
                postalcode=request.data['postalcode']
            )
        address.save()
        customer = Customer.objects.get(user=request.user)
        property = Property(
                customer=customer,
                address=address,
                bathrooms=request.data['bathrooms'],
                bedrooms=request.data['bedrooms'],
                square_feet=request.data['square_feet']
        )
        property.save()
        return Response({'created_property_id': property.id})

class CustomerMortgageCalculatorView(GenericAPIView):
    serializer_class = CustomerMortgageCalculatorSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = CustomerMortgageCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            monthly_interest_rate = (float(serializer.data['yearly_interest_rate'])/100)/12
            power = (1 + monthly_interest_rate)**(float(serializer.data['loan_program_payments'])*-1)
            fromOne = 1 - power
            res = (monthly_interest_rate / fromOne) * (float(serializer.data['home_price']) - float(serializer.data['down_payment']))
            monthly_insurance = float(serializer.data['yearly_insurance'])/12
            monthly_taxes = float(serializer.data['yearly_taxes'])/12
            data = {
                'taxes_payment': monthly_taxes,
                'insurance_payment': monthly_insurance,
                'p&i': res,
                'total_payment': res + monthly_insurance + monthly_taxes

            }
            return Response(data)
        else:
            return Response(serializer.errors)

class CustomerEventSlotViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsCustomer)
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
    pagination_class = None
    logger = logging.getLogger('CustomerEventSlotViewSet')

    def get_queryset(self):
        realtor_users = []
        customer = self.request.user.customer
        for requirement in customer.requirements.all():
            realtor_users.append(requirement.realtor.user)

        queryset = self.queryset.filter(
            Q(requested_by__in=realtor_users, buyer=self.request.user) |
            Q(requested_by=self.request.user)|
            Q(additional_attendees__in=[self.request.user,])|
            Q(property__customer__user=self.request.user)).distinct()
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
            'addresss': request.user.customer\
            .properties.values_list('address__street', 'id')
        })


class CustomerProfileViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsCustomer)
    queryset = Customer.objects.all()
    serializer_class = CustomerPortalSerializer
    logger = logging.getLogger('CustomerProfileViewSet')

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
        customer = request.user.customer
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = request.user.customer
        serializer = self.get_serializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        self.logger.info(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        customer = request.user.customer
        serializer = self.get_serializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        self.logger.info(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
