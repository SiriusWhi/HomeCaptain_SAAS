from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from apps.hcauth.mixins import RecommendMixin
from apps.util.models import (
    HomeCaptainAbstractBaseModel,
    AbstractCertificationModel,
    Address
)
from apps.hcauth.models import Discourage, Recommend

class Concierge(HomeCaptainAbstractBaseModel, RecommendMixin):
    name = models.CharField(max_length=64, blank=True, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discourages_received = GenericRelation(Discourage,
                                           content_type_field='discouraged_content_type',
                                           object_id_field='discouraged_object_id',)
    recommendations_received = GenericRelation(Recommend,
                                               content_type_field='recommended_content_type',
                                               object_id_field='recommended_object_id',)

    def get_realtor_customers(self, realtor_id):
        return self.requirement_set.filter(realtor_id=realtor_id).\
            values(*self.CLIENTS_POPUP_FIELDS)

    def get_loan_officer_customers(self, loan_officer_id):
        return self.requirement_set.filter(loan_officer_id=loan_officer_id).\
            values(*self.CLIENTS_POPUP_FIELDS)

    @property
    def recommend_count(self):
        return self.recommendations_received.count()

    @property
    def discourage_count(self):
        return self.discourages_received.count()
