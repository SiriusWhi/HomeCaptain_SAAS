import datetime
from decimal import Decimal
import uuid

from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

CERTIFICATION_YEAR_CHOICES = [(r,r) for r in
                              range(1979, datetime.date.today().year+1)]
DECIMAL_DEFAULT = Decimal()

class HomeCaptainAbstractBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


    CLIENTS_POPUP_FIELDS = (
        'customer__user__uid', 'customer__user__first_name',
        'customer__user__last_name', 'customer__user__email',
        'customer__milestones', 'customer__buyer_seller', 'customer__uid'
    )
    
    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class GeoCode(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        app_label = 'util'

class Address(HomeCaptainAbstractBaseModel):
    unit_number = models.CharField(max_length=32, blank=True)
    street = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=2, blank=True)
    #TODO: make choices as country ISO codes
    country = models.CharField(max_length=2, default='US')
    postalcode = models.CharField(max_length=16, blank=True)
    
    
    class Meta:
        app_label = 'util'

    #def __str__(self):
    #    return f'{self.street}, {self.city}, {self.state}, {self.zipcode}'

    def get_address_for_geocoding(self):
        return ', '.join([self.unit_number, self.street, self.city, self.state, self.postalcode])
    
class AbstractCertificationModel(HomeCaptainAbstractBaseModel):
    
    CERTIFICATION_NAME_CHOICES = []
    CERTIFYING_BODY_CHOICES = []
    
    name = models.CharField(max_length=256, choices=CERTIFICATION_NAME_CHOICES)
    year = models.IntegerField(choices=CERTIFICATION_YEAR_CHOICES,
                               default=datetime.date.today().year)
    certifying_body = models.CharField(max_length=128,
                                       choices=CERTIFYING_BODY_CHOICES)

    class Meta:
        abstract = True


# class PropertyType(HomeCaptainAbstractBaseModel):
#     name = models.CharField(max_length=128)
#     #if applicable and required we can define the following
#     #feature1
#     #feature2
    
#     def __str__(self):
#         return f'{self.name}'

class RealtorInterest(models.Model):
    interest = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.interest}'

class SMS(HomeCaptainAbstractBaseModel):
    to = models.CharField(max_length=16)
    message = models.CharField(max_length=150)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_smses',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    sent_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_smses',
                                blank=True, null=True, on_delete=models.SET_NULL)
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.to} - {self.message}'

class SalesforceStatus(HomeCaptainAbstractBaseModel):
    message = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=256, blank=True)
    status = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=512, blank=True)
    resource_name = models.CharField(max_length=512, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return f'{self.message}'

    
class HCOutGoingEmail(HomeCaptainAbstractBaseModel):
    to = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
    subject = models.CharField(max_length=512)
    template_name = models.CharField(max_length=256, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_emails',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    sent = models.BooleanField(default=True)
    error = models.TextField(blank=True)
    anymail_message_id = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return f'{self.to} - {self.template_name}'
    
