from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from localflavor.us.models import USStateField
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from apps.hcauth.models import (
    Archive,
    Discourage,
    Recommend,
)
from apps.util.models import HomeCaptainAbstractBaseModel, DECIMAL_DEFAULT
from apps.util.mixins import UserModelLinkMixin
from apps.hcauth.mixins import FavoriteMixin
from apps.hcauth.models import Archive

from django.contrib.contenttypes.fields import GenericRelation

from apps.util.picklists import (
    RATING_CHOICES, MILESTONES_CHOICES,
    MILESTONE_STATUS_REASON_CHOICES, ACCOUNT_TYPE_CHOICES,
    TASK_DROPDOWN_CHOICES, BUYER_SELLER_CHOICES
)

from apps.hcauth.models import Archive

# class HCCharField(models.CharField):
#      salesforce_field_name = "Salesforce Field Name"

#      def __init__(self, salesforce_field_name="", *args, **kwargs):
#          self.salesforce_field_name = salesforce_field_name
#          kwargs['max_length'] = 128
#          super().__init__(*args, **kwargs)


class Customer(UserModelLinkMixin, FavoriteMixin, HomeCaptainAbstractBaseModel):
    """
    Customer (buyer or seller) is stored in the Account Model in salesforce
    with account type as blank
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_mls_auto_created = models.BooleanField(default=False)

    velocify_milestone_id = models.FloatField(null=True, blank=True)
    source_lead_id = models.CharField(max_length=32, blank=True)
    send_realtor_status_email = models.BooleanField(null=True)
    seller = models.BooleanField(null=True)
    realtor_unresponsive = models.BooleanField(null=True)
    realtor_feedback = models.TextField(blank=True)
    real_estate_agent_confirmed = models.BooleanField(null=True)
    real_estate_agent_assigned = models.BooleanField(null=True)
    pre_approval_granted = models.BooleanField(null=True)
    pre_approval_amount = models.FloatField(null=True, blank=True)
    owner_id = models.CharField(max_length=36, blank=True)
    lo_has_been_briefed = models.BooleanField(null=True)
    lead_status = models.CharField(max_length=32, blank=True)
    lead_number = models.CharField(max_length=36, blank=True)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    last_activity_date = models.DateField(null=True)
    last_activity = models.DateField(null=True)
    last_action = models.CharField(max_length=256, blank=True)
    hc_realtor_cs = models.CharField(max_length=256, blank=True)
    hc_realtor_comments = models.CharField(max_length=2048, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=0, default=DECIMAL_DEFAULT)
    
    task_dropdown = models.CharField(max_length=64, blank=True, choices=TASK_DROPDOWN_CHOICES)
    milestones = models.CharField(max_length=128, blank=True, choices=MILESTONES_CHOICES)
    milestone_status_reason = models.CharField(max_length=64, blank=True, choices=MILESTONE_STATUS_REASON_CHOICES)
    #
    hc_realtor_responsiveness = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    hc_realtor_rating = models.IntegerField(blank=True, null=True)
    hc_realtor_knowledge = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    hc_lo_responsiveness = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    hc_lo_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    hc_lo_knowledge = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    hc_lo_cs = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    customer_realtor_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    customer_realtor_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    customer_lo_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    customer_hc_rep_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    #
    buyer_seller = models.CharField(max_length=16, blank=True, choices=BUYER_SELLER_CHOICES)
    account_type = models.CharField(max_length=16, blank=True, choices=ACCOUNT_TYPE_CHOICES)

    ## missing fields begin -->
    ## from Gurpreet Dec 22nd 2018
    realtor_lo_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    realtor_hc_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    lo_realtor_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    lo_hc_rep_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    hc = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)
    customer_realtor_used_as_agent = models.BooleanField(null=True)
    customer_lo_used = models.BooleanField(null=True)
    ## <-- missing fields end

    ##adding missing fields as note by Gurpreet on Dec 24th 2018
    account_at_risk = models.BooleanField(null=True)
    ##added missing fields above


    hc_lo_comments = models.CharField(max_length=2048, blank=True)
    hc_general_comments = models.TextField(blank=True)
    gift_card_sent_date = models.DateField(null=True, blank=True)
    estimated_closing_date = models.DateField(null=True, blank=True)
    do_not_sms = models.BooleanField(null=True)
    date_closed = models.DateField(null=True, blank=True)
    customer_still_searching = models.BooleanField(null=True)
    customer_realtor_comments = models.TextField(blank=True)
    customer_rating_comments = models.CharField(max_length=2048, blank=True)
    customer_nps = models.DecimalField(decimal_places=0, max_digits=12, default=DECIMAL_DEFAULT)
    customer_lo_comments = models.TextField(blank=True)
    customer_hc_rep_comments = models.TextField(blank=True)
    customer_general_comments = models.CharField(max_length=2048, blank=True)
    customer_feedback = models.TextField(blank=True)
    customer_closed = models.BooleanField(null=True)
    current_status = models.CharField(max_length=128, blank=True)
    created_date = models.DateTimeField(blank=True, null=True)
    company = models.CharField(max_length=128, blank=True)
    comments_for_banks = models.TextField(blank=True)
    closing_documents_received = models.BooleanField(null=True)
    cash_back_amount = models.CharField(max_length=32, blank=True)
    buyer = models.BooleanField(null=True)
    bank_name_account = models.CharField(max_length=128, blank=True)
    account_lost = models.BooleanField(null=True)
    #assigned rep is requirement.concierge or property.concierge
    #desired city, state, description are in requirement

    languages_spoken = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)

    # """
    # this is the flag for admin to set. when true, it will show status update required 
    # on dashboard. when the status is changed (updated), this has to be set to false with it
    # so the request json should contain needs_update = false if the realtor is updating the status
    # """
    # needs_update = models.BooleanField(default=False, null=True)


    discourages_received = GenericRelation(Discourage,
                                           content_type_field='discouraged_content_type',
                                           object_id_field='discouraged_object_id',)
    recommendations_received = GenericRelation(Recommend,
                                               content_type_field='recommended_content_type',
                                               object_id_field='recommended_object_id',)
    
    archived_entities= GenericRelation(Archive,
                                       content_type_field='archiving_content_type',
                                       object_id_field='archiving_object_id')    
        
    @property
    def scheduled_showings(self):
        """
        this is to get the scheduled showings that this customer/buyer requested for
        or their realtor did, for them, where they are listed as buyer
        """
        q1 = self.user.requested_events.all()
        q2 = self.user.buyer_showings.all()
        queryset = q1 | q2
        return {
            'count': queryset.count(),
            'showings': [e.get_serialized_event() for e in queryset.all()]
        }
    
    history = HistoricalRecords()

    @property
    def customer_favorite_count(self):
        return self.get_favorite_count()
    
    def get_favorite_count(self):
        return self.user.favorite_property.count()

    @property
    def favorite_properties(self):
        return self.get_favorites()
    
    def get_favorites(self):
        favorite_properties = []
        ##Note: Can't import property serializer here because it creates cyclic import issue
        ##so need to serialize by hand
        for prop in self.user.favorite_property.all():
            favorite_properties.append(prop.partial_serialized_form)
        return favorite_properties

    def create_update_request(self, **kwargs):
        status_update = self.update_history.create(**kwargs)
        user = kwargs.get('requested_by', None)
        if not user:
            status_update.is_auto_created = True
        status_update.save()
        return status_update
        
    def close_update_request(self, new_milestones_value, pk=None, user=None):
        if pk:
            try:
                last_update_request = self.update_history.get(is_updated=False, pk=pk)
            except self.update_history.model.DoesNotExist:
                return None
        else:
            update_history = self.update_history.filter(is_updated=False).order_by('-created')
            if update_history.exists():
                last_update_request = update_history[0]
            else:
                last_update_request = self.create_update_request(requested_by=user)
                
        last_update_request.closed_by = user
        last_update_request.previous_milestone = self.milestones
        last_update_request.is_updated = True
        
        self.milestones = new_milestones_value
        self.save()
        
        last_update_request.save()
        
        return last_update_request

    @property
    def update_request_type(self):
        return list(set([update.request_type for update in self.update_history.filter(is_updated=False)]))
    
    @property
    def customer_update_history(self):
        return [
            {
                'request_type': status_update.request_type,
                'is_updated': status_update.is_updated,
                'requested_by': status_update.requested_by.username if getattr(status_update, 'requested_by', None)  else '',
                'closed_by': status_update.closed_by.username if getattr(status_update, 'closed_by', None) else '',
                'previous_milestone': status_update.previous_milestone,
                'is_auto_created': status_update.is_auto_created,
                'valuation': status_update.valuation,
                'pre_qualification_amount': status_update.pre_qualification_amount,
                'pre_qualification_expiry': status_update.pre_qualification_expiry,
                'notes': status_update.notes,
            }
            for status_update in self.update_history.order_by('-created').all()
        ]

    @property
    def recommend_count(self):
        return self.recommendations_received.count()

    @property
    def discourage_count(self):
        return self.discourages_received.count()

    ##METHODS to work with realtor archival
    def get_realtor_content_type(self):
        from apps.realtor.models import Realtor
        return ContentType.objects.get_for_model(Realtor)

    @property
    def archived_realtors(self):
        return self.archived_entities.filter(
            archived_content_type=self.get_realtor_content_type())

    def add_realtor_to_archive(self, realtor_id):
        archive, created = Archive.objects.get_or_create(
            archiving_content_type=self.content_type,
            archiving_object_id=self.id,
            archived_content_type=self.get_realtor_content_type(),
            archived_object_id=realtor_id)
        archive.save()
        return archive

    def remove_realtor_from_archive(self, realtor_id):
        try:
            archive = Archive.objects.get(
                archiving_content_type=self.content_type,
                archiving_object_id=self.id,
                archived_content_type=self.get_realtor_content_type(),
                archived_object_id=realtor_id)
            archive.delete()
            return True
        except Archive.DoesNotExist:
            return False

    ##METHODS to work with property archival
    def get_property_content_type(self):
        from apps.property.models import Property
        return ContentType.objects.get_for_model(Property)

    @property
    def archived_properties(self):
        return self.archived_entities.filter(
            archived_content_type=self.get_property_content_type())

    def add_property_to_archive(self, property_id):
        archive, created = Archive.objects.get_or_create(
            archiving_content_type=self.content_type,
            archiving_object_id=self.id,
            archived_content_type=self.get_property_content_type(),
            archived_object_id=property_id)
        archive.save()
        return archive

    def remove_property_from_archive(self, property_id):
        try:
            archive = Archive.objects.get(
                archiving_content_type=self.content_type,
                archiving_object_id=self.id,
                archived_content_type=self.get_property_content_type(),
                archived_object_id=property_id)
            archive.delete()
            return True
        except Archive.DoesNotExist:
            return False
        
    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)
          
    ##METHODS to work with concierge archival

    def get_concierge_content_type(self):
        from apps.concierge.models import Concierge
        return ContentType.objects.get_for_model(Concierge)

    @property
    def archived_concierges(self):
        return self.archived_entities.filter(
            archived_content_type=self.get_concierge_content_type())


    def add_concierge_to_archive(self, concierge_id):
        archive, created = Archive.objects.get_or_create(
            archiving_content_type=self.content_type,
            archiving_object_id=self.id,
            archived_content_type=self.get_concierge_content_type(),
            archived_object_id=concierge_id)
        archive.save()
        return archive

    def remove_concierge_from_archive(self, concierge_id):
        try:
            archive = Archive.objects.get(
                archiving_content_type=self.content_type,
                archiving_object_id=self.id,
                archived_content_type=self.get_concierge_content_type(),
                archived_object_id=concierge_id)
            archive.delete()
            return True
        except Archive.DoesNotExist:
            return False

    ##METHODS to work with loan officer archival
    
    def get_loan_officer_content_type(self):
        from apps.lender.models import LoanOfficer
        return ContentType.objects.get_for_model(LoanOfficer)

    @property
    def archived_loan_officers(self):
        return self.archived_entities.filter(
            archived_content_type=self.get_loan_officer_content_type())


    def add_loan_officer_to_archive(self, loan_officer_id):
        archive, created = Archive.objects.get_or_create(
            archiving_content_type=self.content_type,
            archiving_object_id=self.id,
            archived_content_type=self.get_loan_officer_content_type(),
            archived_object_id=loan_officer_id)
        archive.save()
        return archive

    def remove_loan_officer_from_archive(self, loan_officer_id):
        try:
            archive = Archive.objects.get(
                archiving_content_type=self.content_type,
                archiving_object_id=self.id,
                archived_content_type=self.get_loan_officer_content_type(),
                archived_object_id=loan_officer_id)
            archive.delete()
            return True
        except Archive.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.user.username}"

    @property
    def current_requirement(self):
        ##FIXME: need to work more on this to make things easier in backend
        return self.requirements.all()[0]


class CustomerUpdate(HomeCaptainAbstractBaseModel):
    """
    Whenever there is an update required for a customer. The admin will create an object
    of this model. Once created a notification should go out and also.
    Whenever the status/milestones field is updated on Customer, this needs to save the 
    previous value and create a row.
    """
    request_type = models.CharField(max_length = 64, choices = (
        ('Status Update', 'Status Update'),
        ('Pre Qualification Request', 'Pre Qualification Request'),
        ('Valuation Request', 'Valuation Request'),
        ('Realtor Requested', 'Realtor Requested'),
    ), default = 'Status Update')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='update_history')

    ##slight intentional denormalization, to accomodate customer status and requirement, property requests in one model
    requirement = models.ForeignKey('requirement.Requirement', on_delete=models.CASCADE,
                                    related_name='update_history', null=True, blank=True)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE,
                                 related_name='update_history', null=True, blank=True)
    ##
    
    is_updated = models.BooleanField(default=False)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name='customerstatusupdaterequests_created')
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                  on_delete=models.SET_NULL,
                                  related_name='customerstatusupdaterequests_closed')
    previous_milestone = models.CharField(max_length=128, blank=True,
                                          choices=MILESTONES_CHOICES)
    is_auto_created = models.BooleanField(default=False, null=True)
    valuation = models.DecimalField(max_digits=12, decimal_places=0, default=DECIMAL_DEFAULT)
    pre_qualification_amount = models.DecimalField(max_digits=12, decimal_places=0, default=DECIMAL_DEFAULT)
    pre_qualification_expiry = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.customer.user.username} - {self.is_updated} - {self.request_type}"
