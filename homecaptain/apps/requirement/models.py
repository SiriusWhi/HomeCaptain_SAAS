from decimal import Decimal
from django.conf import settings
from django.db import models

from simple_history.models import HistoricalRecords
from actstream.actions import follow

from apps.util.models import HomeCaptainAbstractBaseModel
from apps.customer.models import Customer
from apps.concierge.models import Concierge
from apps.lender.models import LoanOfficer
from apps.realtor.models import Realtor

DECIMAL_DEFAULT = Decimal()

class Requirement(HomeCaptainAbstractBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requirements' )
    concierge = models.ForeignKey(Concierge, null=True, on_delete=models.SET_NULL)
    loan_officer = models.ForeignKey(LoanOfficer, null=True, on_delete=models.SET_NULL,
                                     related_name='requirements')
    realtor = models.ForeignKey(Realtor, null=True, on_delete=models.SET_NULL)

    desired_city_1 = models.CharField(max_length=128, blank=True)
    desired_state_1 = models.CharField(max_length=64, blank=True)
    desired_city_2 = models.CharField(max_length=128, blank=True)
    desired_state_2 = models.CharField(max_length=64, blank=True)
    desired_city_3 = models.CharField(max_length=128, blank=True)
    desired_state_3 = models.CharField(max_length=64, blank=True)
    desired_property_description = models.TextField(blank=True)
    target_price_minimum = models.DecimalField(max_digits=12, decimal_places=0,
                                               default=DECIMAL_DEFAULT)
    target_price_maximum = models.DecimalField(max_digits=12, decimal_places=0,
                                               default=DECIMAL_DEFAULT)
    square_feet = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    
    ##adding missing fields as note by Gurpreet on Dec 24th 2018
    realtor_client_contact_date = models.DateField(null=True, blank=True)
    realtor_lo_comments = models.TextField(blank=True)
    realtor_rating_commnet = models.TextField(blank=True)
    realtor_hc_comments = models.TextField(blank=True)
    lo_realtor_comments = models.TextField(blank=True)
    lo_rating_comment = models.TextField(blank=True)
    lo_hc_comments = models.TextField(blank=True)
    customer_rating_comments = models.TextField(blank=True)
    realtor_general_comments = models.TextField(blank=True)
    customer_general_comments = models.TextField(blank=True)
    lo_general_comments = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    lo_feedback = models.TextField(blank=True)
    ##added missing fields above

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.customer.user.username}"

    @classmethod
    def get_realtor_loan_officer_customers(cls, realtor, loan_officer):
        """
        This method returns all customers who are connected with the given
        relator and loan_officer
        """
        customers = []
        for requirement in cls.objects.filter(realtor=realtor, loan_officer=loan_officer):
            customer.append({
                'uid': requirement.customer.uid,
                'first_name': requirement.customer.first_name,
            })
        return customers
