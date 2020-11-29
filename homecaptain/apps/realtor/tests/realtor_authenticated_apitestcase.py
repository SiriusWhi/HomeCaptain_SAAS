from rest_framework.test import APITestCase

from model_mommy import mommy

from apps.hcauth.models import HomeCaptainUser
from ..models import Realtor, Broker
from apps.property.models import Property
from apps.event.models import Event
from apps.customer.models import Customer
from apps.concierge.models import Concierge
from apps.util.models import Address
from apps.lender.models import Lender, LoanOfficer
from apps.requirement.models import Requirement

class RealtorAuthenticatedAPITestCase(APITestCase):
    loan_officer_user = None
    loan_officer = None
    lender = None
    lender_address = None
    customer_user = None
    customer = None
    concierge_user = None
    concierge = None
    broker = None
    broker_address = None
    realtor_user = None
    realtor = None
    key = ''
    r_property = None
    r_property_address = None
    requirement = None
    agenda = None
    def setUp(self):
        self.r_property_address = mommy.make(Address)
        self.lender_address = mommy.make(Address)
        self.broker_address = mommy.make(Address)
        self.lender = mommy.make(Lender, address= self.lender_address)

        self.loan_officer_user = mommy.make(HomeCaptainUser)
        self.loan_officer = mommy.make(LoanOfficer, user=self.loan_officer_user, lender=self.lender)
        

        #Reusable data

       


        self.customer_user = mommy.make(HomeCaptainUser)
        self.customer = mommy.make(Customer, user=self.customer_user, uid="b624426d-3f1d-4159-a5da-982a3c11c478", buyer_seller="Both", milestones='Customer Still Searching for home')

        self.concierge_user = mommy.make(HomeCaptainUser)
        self.concierge = mommy.make(Concierge, user=self.concierge_user, uid="b624426d-3f1d-4159-a5da-982a3c11c478")
        self.broker=mommy.make(Broker, address=self.broker_address)
        self.realtor_user = mommy.make(HomeCaptainUser,
                username='realtor',
                first_name='Realtor',
                email='realtor@realtor.com',
                uid = '2542c60b-54e0-4b0d-9d64-bac003967f95',
                salesforce_id = 'f7ef58fc-2702-48b1-96e2-1de7d58ad492'
            )
        self.realtor = mommy.make(Realtor, broker=self.broker, user=self.realtor_user, uid="b624426d-3f1d-4159-a5da-982a3c11c478")

         # Authenticate as realtor

        self.realtor_user.set_password('realtor1')
        self.realtor_user.save()
        data = {
                    'username': self.realtor.user.username,
                    'email': self.realtor.user.email,
                    'password': 'realtor1'
                }
        res = self.client.post('/api/auth/login/', data=data, format='json')
        self.key = res.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.key)

        self.r_property = mommy.make(Property, address=self.r_property_address, customer=self.customer, concierge=self.concierge, realtor=self.realtor, loan_officer=self.loan_officer)
        self.requirement = mommy.make(Requirement, customer=self.customer, realtor=self.realtor, concierge=self.concierge, loan_officer=self.loan_officer)
        self.agenda = mommy.make(Event, property=self.r_property, buyer=self.customer.user, requested_by=self.realtor.user)