from uuid import uuid4
from decimal import Decimal
from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder

import googlemaps

from apps.util.picklists import (
    PROPERTY_TYPE_CHOICES,
    PROPERTY_SUB_TYPE_CHOICES
)
from simple_history.models import HistoricalRecords
from apps.util.models import (
    HomeCaptainAbstractBaseModel,
    Address,
)
from apps.hcauth.mixins import FavoritedMixin, RecommendMixin
from apps.customer.models import Customer
from apps.lender.models import LoanOfficer
from apps.realtor.models import Realtor
from apps.concierge.models import Concierge
from apps.util.utils import upload_image_to_s3, get_s3_url_for_key

DECIMAL_DEFAULT = Decimal()

def get_placeholder_uuid():
    return str(uuid4())

class Property(HomeCaptainAbstractBaseModel, FavoritedMixin, RecommendMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="properties")
    concierge = models.ForeignKey(Concierge, null=True, on_delete=models.SET_NULL)
    realtor = models.ForeignKey(Realtor, null=True, on_delete=models.SET_NULL)
    loan_officer = models.ForeignKey(LoanOfficer, null=True, on_delete=models.SET_NULL)
    is_mls_auto_created = models.BooleanField(default=False)
    
    valuation = models.DecimalField(max_digits=12, decimal_places=0, default=DECIMAL_DEFAULT)

    favorite_count = models.IntegerField(default=0, blank=True, null=True)

    """BEGIN MLS FIELDS"""
    ##properties that are created on HC will have placeholder uid as listing_key
    listing_key = models.CharField(max_length=36, unique=True, default=get_placeholder_uuid)
    modification_timestamp = models.DateTimeField(blank=True, null=True)
    property_type = models.CharField(max_length=64, blank=True,
                                     default='Residential',
                                     choices = PROPERTY_TYPE_CHOICES)
    property_sub_type = models.CharField(max_length=64, blank=True, default='',
                                         choices=PROPERTY_SUB_TYPE_CHOICES)
    address = models.OneToOneField(Address, on_delete=models.PROTECT, null=True)
    listing_url = models.URLField(max_length=512, blank=True)
    lead_routing_email = models.EmailField(blank=True)
    listing_category = models.CharField(max_length=32, blank=True)
    #photos = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)

    disclose_address = models.BooleanField(default=True)
    permit_address_on_internet = models.BooleanField(default=True)
    vow_address_display = models.BooleanField(default=True)
    
    listing_description = models.TextField(blank=True)
    #supposed to be unique but properties that are created on HC will not have it
    mls_number = models.CharField(max_length=36, default=get_placeholder_uuid)
    lot_size = models.FloatField(default=0.0)
    listing_date = models.DateField(blank=True, null=True)
    listing_title = models.CharField(max_length=256, blank=True)

    target_price_maximum = models.IntegerField(default=0)
    target_price_minimum = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    year_built = models.IntegerField(blank=True, null=True)
    full_bathrooms = models.IntegerField(default=0)
    three_quarter_bathrooms = models.IntegerField(default=0)
    half_bathrooms = models.IntegerField(default=0)
    one_quarter_bathrooms = models.IntegerField(default=0)
    square_feet = models.IntegerField(default=0)

    foreclosure_status = models.CharField(max_length=64, blank=True)
    listing_participants = JSONField(encoder=DjangoJSONEncoder,
                                     blank=True, null=True)
    brokerage = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
    ##we probably won't use it and use Google geocode api with address
    location =  JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
    open_houses = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
    taxes = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
    expenses = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
    detailed_characteristics = JSONField(encoder=DjangoJSONEncoder,
                                         blank=True, null=True)
    strike = models.IntegerField(default=0, choices=((1,1), (2,2), (3,3)))
    """END MLS FIELDS"""

    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.listing_key}"

    def save(self, *args, **kwargs):
        if not (self.disclose_address and \
                self.permit_address_on_internet and \
                self.vow_address_display):
            #strict requirement from LISTHUB
            if self.address:
                self.address.unit_number = ''
                self.address.street = ''
                self.address.save()
        ##NOT USED. USING GEOCDE.IO IN FRONTEND
        ##FIXME: google geocode API is timing out! need a paid service!!
        ##elif self.address:
        ##    self.set_geocode()
        return super(Property, self).save(*args, **kwargs)

    ##NOT USED. USING GEOCDE.IO IN FRONTEND
    # def set_geocode(self):
    #     if not (self.lat and self.lng):
    #         gmaps = googlemaps.Client(key=settings.GOOGLE_GEOCODING_API_KEY)
    #         geocode_result = gmaps.geocode(self.address.get_address_for_geocoding())
    #         if len(geocode_result)>0:
    #             geocode = geocode_result[0]['geometry']['location']
    #             self.lat = geocode['lat']
    #             self.lng = geocode['lng']
    #             self.save()

    @property
    def photo_count(self):
        return self.photos.count()
        
    def get_photo_url_by_uid(self, uid):
        try:
            photo = self.photos.get(uid=uid)
            return photo.s3_url()
        except self.photos.model.DoesNotExist:
            return ''

    @property
    def partial_serialized_form(self):
        return  {
            "id": self.id,
            "uid": self.uid,
            "address": self.address.street,
            "bathrooms": self.bathrooms,
            "bedrooms": self.bedrooms,
            "square_feet": self.square_feet,
            "target_price_minimum": self.target_price_minimum,
            "target_price_maximum": self.target_price_maximum,
            "realtor": {
                "user_uid" : self.realtor.user.uid,
                "first_name": self.realtor.user.first_name,
                "username": self.realtor.user.username
            },
            "loan_officer": {
                "user_uid": self.loan_officer.user.uid,
                "first_name": self.loan_officer.user.first_name,
                "username": self.loan_officer.user.username
            },
            "concierge": {
                "user_uid": self.concierge.user.uid,
                "first_name": self.concierge.user.first_name,
                "username": self.concierge.user.username
            },
        }

    @property
    def scheduled_showings(self):
        """
        this is to get the scheduled showing of this property that are in future
        this is probably needed where the property is listed 
        when the # of showings are clicked, it will show the list of buyers or realtors
        who have requested the showings, with realtor first_name, uid, realtor.user.uid,
        and some agenda/showing details.
        """
        ##FIXME: later this has to be filtered on is_confirmed=True
        queryset = self.events.filter(proposed_start__gt=datetime.now())
        return {
            'count': queryset.count(),
            'showings': [e.get_serialized_event() for e in queryset.all()]
        }
    
    @property
    def property_favorite_count(self):
        return self.get_favorite_count()
    
    def get_favorite_count(self):
        self.favorite_count = self.favorite_users.count()
        self.save()
        return self.favorite_count

    @property
    def favoriting_buyers(self):
        return self.get_favorites()
    
    def get_favorites(self):
        favorite_users = []
        for user in self.favorite_users.all():
            favorite_users.append({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "milestones": user.customer.milestones,
                "uid": user.uid
            })
        return favorite_users
            
    

                
# class FavoriteProperty(HomeCaptainAbstractBaseModel):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = (("property", "customer"),)
    
#     def __str__(self):
#         return f"{self.property.uid}, {self.customer.user.username}"


class PropertyPhoto(HomeCaptainAbstractBaseModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,
                                 related_name='photos')
    media_modification_timestamp = models.DateTimeField()
    media_url = models.URLField(max_length=256)
    media_caption = models.CharField(max_length=256, blank=True)
    media_description = models.TextField(blank=True)
    key = models.CharField(max_length=48, blank=True)
    is_in_s3 = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Photo id: {self.id}, Property id: {self.property.id}"

    def s3_url(self):
        if not self.is_in_s3:
            response = upload_image_to_s3(self.media_url, str(self.uid))
            if response.get('key', None) and response.get('url', None):
                self.is_in_s3 = True
                self.key = response['key']
                self.save()
                return response['url']
            else:
                return {"error": "Exception in Upload to S3"}
        else:
            response = get_s3_url_for_key(self.key)
            if response.get('key', None) and response.get('url', None):
                return response['url']
            else:
                return {"error": "Exception in getting S3 URL"}
