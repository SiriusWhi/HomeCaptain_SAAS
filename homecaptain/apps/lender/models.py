from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from apps.hcauth.models import Archive
from apps.util.models import (HomeCaptainAbstractBaseModel,
                              AbstractCertificationModel,
                              Address,)
from apps.util.picklists import (
    RATING_CHOICES, MILESTONES_CHOICES,
    MILESTONE_STATUS_REASON_CHOICES, ACCOUNT_TYPE_CHOICES,
    TASK_DROPDOWN_CHOICES, LEADSOURCE_CHOICES, TITLEE_CHOICES
)
from apps.hcauth.mixins import RecommendMixin
from apps.hcauth.models import Discourage, Recommend

class Lender(HomeCaptainAbstractBaseModel):
    """
    Lender is srtored in the Account Model in salesforce
    with account type as 'Customer'
    """
    website = models.URLField(blank=True)
    #type = customer
    salesforce_id = models.CharField(max_length=36, unique=True)
    phone = models.CharField(max_length=16, blank=True) #accomodating as per the data from prod
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.name or self.website or self.salesforce_id}"

class LenderAdmin(HomeCaptainAbstractBaseModel):
    lender = models.OneToOneField(Lender, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='lender_admin')
    sf_account_id = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return f"{self.user.email} ({self.lender.name})"

class LenderCertification(AbstractCertificationModel):
    lender = models.OneToOneField(Lender, on_delete=models.CASCADE)
    
    CERTIFYING_BODY_CHOICES = (
        ('lender_certifying_body_1', 'Lender Certifying Body 1'),
    )

    CERTIFICATION_NAME_CHOICES = (
        ('lender_certification_1', 'Lender Certification 1'),
    )

    def __str__(self):
        return f"{self.name} ({self.lender.name})"

    
class LoanOfficer(HomeCaptainAbstractBaseModel):
    """
    LoanOfficer is stored in the Contact object with lender as the reference to 
    Account model
    """
    lender = models.ForeignKey(Lender, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='loan_officer')


    velocify_milestone_id = models.FloatField(null=True, blank=True)
    titlee = models.CharField(max_length=128, blank=True, choices=TITLEE_CHOICES)
    title = models.CharField(max_length=128, blank=True)
    record_type_id = models.CharField(max_length=36, blank=True)
    owner_id = models.CharField(max_length=36, blank=True)
    new_score = models.IntegerField(default=0)
    lead_source = models.CharField(max_length=128, blank=True, choices=LEADSOURCE_CHOICES)
    lead_number = models.CharField(max_length=36, blank=True)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    franchisee = models.BooleanField(null=True)
    do_not_sms = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    credit_lead_name = models.CharField(max_length=128, blank=True)
    credit_lead_converter = models.CharField(max_length=128, blank=True)
    created_date = models.DateTimeField(null=True)
    comments_reviews = models.TextField(blank=True)
    average_of_lo_realtor_rating = models.FloatField(default=0.0)
    approval_status = models.CharField(max_length=128, blank=True)
    
    
    ##adding missing fields as note by Gurpreet on Dec 24th 2018
    lo_nps = models.IntegerField(null=True, blank=True)
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
    
    archived_entities= GenericRelation(Archive,
                                       content_type_field='archiving_content_type',
                                       object_id_field='archiving_object_id')

    def __str__(self):
        return f"{self.user.username} ({self.lender.name})"

    def get_realtor_customers(self, realtor_id):
        return self.requirements.filter(realtor_id=realtor_id).values(*self.CLIENTS_POPUP_FIELDS)

    @property
    def recommend_count(self):
        return self.recommendations_received.count()

    @property
    def discourage_count(self):
        return self.discourages_received.count()

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

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
        return ContentType.objects.get_for_model(self.requirements.model)
   
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


class LoanOfficerCertification(AbstractCertificationModel):
    loan_officer = models.OneToOneField(LoanOfficer, on_delete=models.CASCADE)
    
    CERTIFYING_BODY_CHOICES = (
        ('loan_officer_certifying_body_1', 'Loan Officer Certifying Body 1'),
    )

    CERTIFICATION_NAME_CHOICES = (
        ('loan_officer_certification_1', 'Loan Officer Certification 1'),
    )

    def __str__(self):
        return f"{self.name} ({self.loan_officer.name})"
