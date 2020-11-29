from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from ..models import Customer
from apps.lender.models import Lender, LoanOfficer
from apps.hcauth.models import HomeCaptainUser
from apps.util.models import Address
from apps.customer.models import Customer
from apps.concierge.models import Concierge
from apps.realtor.models import Realtor
from apps.property.models import Property
from apps.event.models import Event

from model_mommy import mommy

class TestCustomerAPI(APITestCase):
    loan_officer_user = None
    loan_officer = None
    lender = None
    customer_user = None
    customer = None
    concierge_user = None
    concierge = None
    realtor_user = None
    realtor = None
    address = None
    key = ''
    r_property = None
    requirement = None
    agenda = None

    def setUp(self):
        self.lender = mommy.make(Lender)
        self.loan_officer_user = mommy.make(HomeCaptainUser,
            username='loan_officer', 
            first_name='Loan Officer',
            email='loanofficer@loanofficer.com', 
            uid = '2542c60b-54e0-4b0d-9d64-bac003967f92',
            salesforce_id = 'f7ef58fc-2702-48b1-96e2-1de7d58ad499'
        )
        self.loan_officer_user.save()
        self.loan_officer = mommy.make(LoanOfficer, user=self.loan_officer_user, lender=self.lender)
    
        self.address = mommy.make(Address)

        self.customer_user = mommy.make(HomeCaptainUser, 
            username='customer', 
            first_name='Customer',
            email='customer@customer.com', 
            uid = '2542c60b-54e0-4b0d-9d64-bac003967f93',
            salesforce_id = 'f7ef58fc-2702-48b1-96e2-1de7d58ad490'
        )
        self.customer_user.set_password('customer_user1')
        self.customer_user.save()
        self.customer = mommy.make(Customer, user=self.customer_user)
        data = {
            'username': self.customer.user.username,
            'email': self.customer.user.email,
            'password': 'customer_user1'
        }
        res = self.client.post('/api/auth/login/', data=data, format='json')
        self.key = res.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.key)

        self.concierge_user = mommy.make(HomeCaptainUser, 
            username='concierge', 
            first_name='Concierge',
            email='concierge@concierge.com', 
            uid = '2542c60b-54e0-4b0d-9d64-bac003967f94',
            salesforce_id = 'f7ef58fc-2702-48b1-96e2-1de7d58ad491'
        )
        self.concierge = mommy.make(Concierge, user=self.concierge_user)

        self.realtor_user = mommy.make(HomeCaptainUser, 
            username='realtor', 
            first_name='Realtor',
            email='realtor@realtor.com', 
            uid = '2542c60b-54e0-4b0d-9d64-bac003967f95',
            salesforce_id = 'f7ef58fc-2702-48b1-96e2-1de7d58ad492'
        )
        self.realtor = mommy.make(Realtor, user=self.realtor_user)

        self.r_property = mommy.make(Property, address=self.address, customer=self.customer, concierge=self.concierge, realtor=self.realtor, loan_officer=self.loan_officer)
        
        self.agenda = mommy.make(Event, property=self.r_property, buyer=self.customer.user, requested_by=self.loan_officer.user)

    # def test_post_agenda(self):
    #     data = {
    #         'name': 'Property Showing',
    #         'note': 'Lake property open house',
    #         'location': 'location1',
    #         'is_seller_required': True,
    #         'is_seller_realtor_required': True,
    #         'is_buyer_required': True,
    #         'is_buyer_loan_officer_required': True,
    #         'is_buyer_realtor_required': True,
    #         'is_buyer_concierge_required': True,
    #         'is_service_provider_required': True,
    #         'proposed_start': '2019-2-14T15:30:30',
    #         'proposed_end': '2019-2-14T17:30:30',
    #         'emails': {},
    #         'requesting_user_type': 'buyer',
    #         'is_confirmed': True,
    #         'property': self.r_property.id,
    #         'buyer': self.customer.user.username,
    #         'requested_by': self.customer.user.id,
    #         'additional_attendees': [
    #             self.concierge.user.username
    #         ]
    #     }
    #     res = self.client.post('/api/customer/agenda/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     data = {
    #         'name': '',
    #         'note': '',
    #         'location': '',
    #         'is_seller_required': True,
    #         'is_seller_realtor_required': True,
    #         'is_buyer_required': True,
    #         'is_buyer_loan_officer_required': True,
    #         'is_buyer_realtor_required': True,
    #         'is_buyer_concierge_required': True,
    #         'is_service_provider_required': True,
    #         'proposed_start': '2019-2-14T15:30',
    #         'proposed_end': '2019-2-14T17:30',
    #         'emails': {},
    #         'requesting_user_type': 'buyer',
    #         'is_confirmed': True,
    #         'property': 0,
    #         'buyer': '',
    #         'requested_by': 0,
    #         'additional_attendees': [
    #
    #         ]
    #     }
    #     res = self.client.post('/api/customer/agenda/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_agenda(self):
        res = self.client.get('/api/customer/agenda/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_agenda_extras(self):
        res = self.client.get('/api/customer/agenda/extras/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_agenda_uid(self):
        res = self.client.get('/api/customer/agenda/'+ str(self.agenda.uid) +'/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get('/api/customer/agenda/XXX/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # def test_put_agenda_uid(self):
    #     data = {
    #             'name': 'Property Showing',
    #             'note': 'Lake property open house',
    #             'location': 'locatio2',
    #             'is_seller_required': True,
    #             'is_seller_realtor_required': True,
    #             'is_buyer_required': True,
    #             'is_buyer_loan_officer_required': True,
    #             'is_buyer_realtor_required': True,
    #             'is_buyer_concierge_required': True,
    #             'is_service_provider_required': True,
    #             'proposed_start': '2019-2-14T15:30:30',
    #             'proposed_end': '2019-2-14T17:30:30',
    #             'emails': {},
    #             'requesting_user_type': 'buyer',
    #             'is_confirmed': True,
    #             'property': self.r_property.id,
    #             'buyer': self.customer.user.username,
    #             'requested_by': self.customer.user.id,
    #             'additional_attendees': [
    #                 self.concierge.user.username
    #             ]
    #         }
    #     res = self.client.put('/api/customer/agenda/' + str(self.agenda.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    # def test_patch_agenda_uid(self):
    #     data = {
    #             'name': 'Property Showing',
    #             'note': 'Lake property open house',
    #             'location': 'locatio3',
    #             'is_seller_required': True,
    #             'is_seller_realtor_required': True,
    #             'is_buyer_required': True,
    #             'is_buyer_loan_officer_required': True,
    #             'is_buyer_realtor_required': True,
    #             'is_buyer_concierge_required': True,
    #             'is_service_provider_required': True,
    #             'proposed_start': '2019-2-14T15:30:30',
    #             'proposed_end': '2019-2-14T17:30:30',
    #             'emails': {},
    #             'requesting_user_type': 'buyer',
    #             'is_confirmed': True,
    #             'property': self.r_property.id,
    #             'buyer': self.customer.user.username,
    #             'requested_by': self.customer.user.id,
    #             'additional_attendees': [
    #                 self.concierge.user.username
    #             ]
    #         }
    #     res = self.client.patch('/api/customer/agenda/' + str(self.agenda.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_agenda_uid(self):
        res = self.client.delete('/api/customer/agenda/' + str(self.agenda.uid) + '/')
        #TODO: verify why this returns 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)   

    def test_get_team_realtor(self):
        res = self.client.get('/api/customer/team/realtor/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_realtor_archived(self):
        res = self.client.get('/api/customer/team/realtor/archived/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_realtor_all(self):
        res = self.client.get('/api/customer/team/realtor/all/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_realtor_stats(self):
        res = self.client.get('/api/customer/team/realtor/stats/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_realtor_uid(self):
        res = self.client.get('/api/customer/team/realtor/' + str(self.realtor.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_archive(self):
        res = self.client.post('/api/customer/team/realtor/' + str(self.realtor.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_restore(self):
        res = self.client.post('/api/customer/team/realtor/' + str(self.realtor.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_discourage(self):
        res = self.client.post('/api/customer/team/realtor/' + str(self.realtor.uid) + '/discourage/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_post_team_realtor_uid_recommend(self):
        res = self.client.post('/api/customer/team/realtor/' + str(self.realtor.uid) + '/recommend/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_request(self):
        res = self.client.post('/api/customer/team/realtor/request/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_send_invite(self):
        data = {
            'message': 'test',
            'user': {
                'first_name': "brenton",
                "last_name": "zhang",
                "email": "brenton@djangoforce.com",
                "phone": "8715445713",
                "user_type": "Realtor"
            }
        }
        res = self.client.post('/api/customer/team/realtor/send_invite/', data=data, format='json')
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_assign(self):
        data = {
            'realtor_uid': self.realtor.uid,
        }
        res = self.client.post('/api/customer/team/realtor/assign/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_team_concierge(self):
        res = self.client.get('/api/customer/team/concierge/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_concierge_archived(self):
        res = self.client.get('/api/customer/team/concierge/archived/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_concierge_stats(self):
        res = self.client.get('/api/customer/team/concierge/stats/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_concierge_uid(self):
        res = self.client.get('/api/customer/team/concierge/' + str(self.concierge.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_concierge_uid_archive(self):
        res = self.client.post('/api/customer/team/concierge/' + str(self.concierge.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_concierge_uid_restore(self):
        res = self.client.post('/api/customer/team/concierge/' + str(self.concierge.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_concierge_uid_discourage(self):
        res = self.client.post('/api/customer/team/concierge/' + str(self.concierge.uid) + '/discourage/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_post_team_concierge_uid_recommend(self):
        res = self.client.post('/api/customer/team/concierge/' + str(self.concierge.uid) + '/recommend/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_listing(self):
        res = self.client.get('/api/customer/listing/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_listing_uid(self):
        res = self.client.get('/api/customer/listing/' + str(self.r_property.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_post_listing_favorite(self):
        res = self.client.post('/api/customer/listing/'  + str(self.r_property.uid) + '/favorite/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_listing_unfavorite(self):
        res = self.client.post('/api/customer/listing/'  + str(self.r_property.uid) + '/unfavorite/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_loan_officer(self):
        res = self.client.get('/api/customer/team/loan-officer/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_loan_officer_archived(self):
        res = self.client.get('/api/customer/team/loan-officer/archived/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_loan_officer_all(self):
        res = self.client.get('/api/customer/team/loan-officer/all/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_loan_officer_stats(self):
        res = self.client.get('/api/customer/team/loan-officer/stats/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_loan_officer_uid(self):
        res = self.client.get('/api/customer/team/loan-officer/' + str(self.loan_officer.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_loan_officer_uid_archive(self):
        res = self.client.post('/api/customer/team/loan-officer/' + str(self.loan_officer.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_loan_officer_uid_restore(self):
        res = self.client.post('/api/customer/team/loan-officer/' + str(self.loan_officer.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_loan_officer_uid_discourage(self):
        res = self.client.post('/api/customer/team/loan-officer/' + str(self.loan_officer.uid) + '/discourage/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_post_loan_officer_uid_recommend(self):
        res = self.client.post('/api/customer/team/loan-officer/' + str(self.loan_officer.uid) + '/recommend/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_loan_officer_uid_assign(self):
        data = {
            'loan_officer_uid': self.loan_officer.uid,
        }
        res = self.client.post('/api/customer/team/loan-officer/assign/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile(self):
        res = self.client.get('/api/customer/profile/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_profile(self):
        data = {
                'id': self.customer.id,
                'uid': self.customer.uid,
                'user': {
                    "uid": self.customer.user.uid,
                    "id":  self.customer.user.id,
                },
                'discourage_count': 0,
                'recommend_count': 0
            }
        res = self.client.put('/api/customer/profile/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_profile(self):
        data = {
                'id': self.customer.id,
                'uid': self.customer.uid,
                'user': {
                    "uid": self.customer.user.uid,
                    "id":  self.customer.user.id,
                },
                'discourage_count': 0,
                'recommend_count': 0
            }
        res = self.client.patch('/api/customer/profile/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
