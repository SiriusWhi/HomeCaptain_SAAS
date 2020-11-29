from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from apps.hcauth.models import Archive
from apps.util.models import (HomeCaptainAbstractBaseModel,
                              AbstractCertificationModel,
                              Address, GeoCode, DECIMAL_DEFAULT)
from apps.util.picklists import TITLEE_CHOICES, REALTOR_INTERESTS_CHOICES

from apps.hcauth.models import Discourage, Recommend

from apps.hcauth.mixins import RecommendMixin


class Broker(HomeCaptainAbstractBaseModel):
    work_history = models.IntegerField(default=0)
    website_1 = models.URLField(blank=True)
    website_2 = models.URLField(blank=True)
    website_3 = models.URLField(blank=True)
    phone = models.CharField(max_length=16, blank=True) #accomodating as per the data from prod
    nar_status = models.TextField(blank=True)
    master_broker_agreement_signed = models.BooleanField(null=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=256, blank=True, unique=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)

    is_mls_auto_created = models.BooleanField(default=False)
    ####Broker ends here as defined in data from SF
    
    def __str__(self):
        return f"{self.company or self.first_name or self.email}"
        

class Realtor(HomeCaptainAbstractBaseModel):
    """
    Realtor is stored in the Contact Model on Salesforce
    With an account reference to a single account named "Realtor"

    Broker is not listed as a reference, rather hard coded as a field with every realtor.
    A realtor can themselves be a broker as well.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='realtor')
    broker = models.ForeignKey(Broker, null=True, on_delete=models.SET_NULL)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True,
                                related_name='realtors')

    is_mls_auto_created = models.BooleanField(default=False)
    
    #name = "Realtor"
    work_history = models.IntegerField(default=0)
    velocify_milestone_id = models.FloatField(null=True, blank=True)
    titlee = models.CharField(max_length=128, blank=True, choices=TITLEE_CHOICES)
    title = models.CharField(max_length=128, blank=True)
    record_type_id = models.CharField(max_length=36, blank=True)
    realtor_unresponsive_count = models.IntegerField(default=0)
    realtor_score = models.DecimalField(max_digits=12, decimal_places=0, default=DECIMAL_DEFAULT)
    owner_id = models.CharField(max_length=36, blank=True)
    number_of_current_leads = models.IntegerField(default=0)
    new_score = models.DecimalField(max_digits=12, decimal_places=0, default=DECIMAL_DEFAULT)
    nar_status = models.TextField(blank=True)
    low_realtor_rating_count_from_lo = models.IntegerField(default=0)
    low_realtor_rating_count_from_customer = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    leads_sent = models.IntegerField(default=0)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    high_realtor_rating_count_from_lo = models.IntegerField(default=0)
    high_realtor_rating_count_from_customer = models.IntegerField(default=0)
    do_not_sms = models.BooleanField(default=False)
    deals_sent = models.IntegerField(default=0)
    created_date = models.DateTimeField(blank=True, null=True)
    counties_served = models.TextField(blank=True)
    comments_reviews = models.TextField(blank=True)
    closings = models.IntegerField(default=0)
    closing_percentage = models.FloatField(null=True, blank=True)
    balcklisted = models.BooleanField(default=False)
    average_customer_realtor_rating = models.IntegerField(default=0)
    approval_status = models.CharField(max_length=64, blank=True)
    military_service = models.CharField(max_length=128, blank=True)
    account_lost_count = models.IntegerField(default=0)


    ##adding missing fields as note by Gurpreet on Dec 24th 2018
    realtor_contact_mobile_phone = models.CharField(max_length=16, blank=True)
    realtor_contact_company_phone = models.CharField(max_length=16, blank=True)
    velocify_realtor_phone = models.CharField(max_length=16, blank=True)
    agent_milestone_end_cycle = models.BooleanField(null=True)
    realtor_nps = models.IntegerField(null=True, blank=True)
    realtor_interests = models.CharField(max_length=32, blank=True, choices=REALTOR_INTERESTS_CHOICES)
    realtor_status_start_date = models.DateField(null=True, blank=True)
    send_realtor_status_e_mail = models.BooleanField(null=True)
    franchisee = models.BooleanField(null=True)
    amount_paid = models.CharField(max_length=16, blank=True)
    simplesms_donotsms = models.BooleanField(default=False)
    ##added missing fields above

    discourages_received = GenericRelation(Discourage,
                                           content_type_field='discouraged_content_type',
                                           object_id_field='discouraged_object_id',)
    recommendations_received = GenericRelation(Recommend,
                                               content_type_field='recommended_content_type',
                                               object_id_field='recommended_object_id',)
    
    #####Realtor ends here as defined in data from SF

    
    
    # full_name = models.CharField(max_length=128, blank=True)
    # #just storing reference not object
    # full_name_formula = models.CharField(max_length=128, blank=True)
    # business_phone = PhoneNumberField(blank=True)
    # contact_email = models.EmailField(blank=True)
    
    # name = models.CharField(max_length=128, blank=True)
    # broker_geocode = models.ForeignKey(GeoCode, null=True, blank=True,
    #                                    on_delete=models.SET_NULL)

    
    # last_activity = models.DateField(null=True, blank=True)
    # geolocation = models.TextField(blank=True)
    # reports_to_id = models.CharField(max_length=128, blank=True)
    

    # average_of_lo_realtor_rating = models.IntegerField(default=0)
    # lead_source = models.CharField(max_length=128, blank=True, choices = (
    #     ('source 1', 'source 1'),
    # ))
    # credit_lead_name = models.CharField(max_length=128, blank=True)
    # lead_number = models.CharField(max_length=64, blank=True)
    # credit_lead_converter = models.CharField(max_length=128, blank=True)
    # contact_description = models.TextField(blank=True)
    # amount_paid = models.CharField(max_length=32, blank=True)


    ##TODO: @brenton - these need to be removed
    #no related_name because the other side- lo - should not be able query
    #for realtors who have archived them
    #archived_loan_officers = models.ManyToManyField('lender.LoanOfficer')
    #archived_concierges = models.ManyToManyField('concierge.Concierge')

    """
    A fallacy iin using just a generic relation is that it just works on ids
    and does not consider the archived content type
    so it will return ids of all objects archived by the realtor
    irrespective of the content type - properies, requirements, loan officers and concierge

    Question: How to get archived entties of a particular type

    Option 1: Use a custom manager on archive
    - might not work, because the archival is per realtor, 
    not global and there will be no way to filter by realtor in custom manager on Archive

    Option 2: So need to define a property on realtor, one for each of the four archived_types 
    and filter on content type in that method, so that content type filter and user filter are both 
    applied
    - using this approach
    """
    archived_entities= GenericRelation(Archive,
                                       content_type_field='archiving_content_type',
                                       object_id_field='archiving_object_id')

    def __str__(self):
        return f"{self.user.username}"

    def is_attached_to_customer(self, customer):
        return self.requirement_set.filter(customer=customer).exists()

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)
    
    @property
    def recommend_count(self):
        return self.recommendations_received.count()

    @property
    def discourage_count(self):
        return self.discourages_received.count()

    ##METHODS to work with property archival
    def get_property_content_type(self):
        return ContentType.objects.get_for_model(self.property_set.model)

    @property
    def archived_properties(self):
        return self.archived_entities.filter(archived_content_type=self.get_property_content_type())
    
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

    ##METHODS to work with requirement archival
    def get_requirement_content_type(self):
        return ContentType.objects.get_for_model(self.requirement_set.model)
   
    @property
    def archived_requirements(self):
        self.archived_entities.filter(archived_content_type=self.get_requirement_content_type())


    def add_requirement_to_archive(self, requirement_id):
        archive, created = Archive.objects.get_or_create(
            archiving_content_type=self.content_type,
            archiving_object_id=self.id,
            archived_content_type=self.get_requirement_content_type(),
            archived_object_id=requirement_id)
        archive.save()
        return archive

    def remove_requirement_from_archive(self, requirement_id):
        try:
            archive = Archive.objects.get(
                archiving_content_type=self.content_type,
                archiving_object_id=self.id,
                archived_content_type=self.get_requirement_content_type(),
                archived_object_id=requirement_id)
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
        return self.archived_entities.filter(archived_content_type=self.get_loan_officer_content_type())

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

    def get_loan_officer_customers(self, loan_officer_id):
        return self.requirement_set.filter(loan_officer_id=loan_officer_id).\
            values(*self.CLIENTS_POPUP_FIELDS)


class RealtorCertification(AbstractCertificationModel):
    realtor = models.OneToOneField(Realtor, on_delete=models.CASCADE,)
    
    def certifying_body_choices():
        return ( ('realtor_certifying_body_1', 'Realtor Certifying Body 1'), )

    def certification_name_choices():
        return ( ('realtor_certification_1', 'Realtor Certification 1'), )

    def __str__(self):
        return f"{self.name} ({self.realtor.user.username})"
