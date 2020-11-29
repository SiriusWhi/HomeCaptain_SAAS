from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from ..models import LoanOfficer, Lender
from apps.hcauth.models import HomeCaptainUser
from apps.util.models import Address
from apps.customer.models import Customer
from apps.concierge.models import Concierge
from apps.realtor.models import Realtor
from apps.property.models import Property
from apps.event.models import Event

from model_mommy import mommy

class TestLoanOfficerAPI(APITestCase):
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
        # Authenticate as loan officer
        self.loan_officer_user = mommy.make(HomeCaptainUser,
            username='loan_officer', 
            first_name='Loan Officer',
            email='loanofficer@loanofficer.com', 
            uid = '2542c60b-54e0-4b0d-9d64-bac003967f92',
            salesforce_id = 'f7ef58fc-2702-48b1-96e2-1de7d58ad499'
        )
        self.loan_officer_user.set_password('loan_officer1')
        self.loan_officer_user.save()
        self.loan_officer = mommy.make(LoanOfficer, user=self.loan_officer_user, lender=self.lender)
        data = {
                'username': self.loan_officer.user.username,
                'email': self.loan_officer.user.email,
                'password': 'loan_officer1'
                }
        res = self.client.post('/api/auth/login/', data=data, format='json')
        self.key = res.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.key)

        #Reusable data

        self.address = mommy.make(Address)

        self.customer_user = mommy.make(HomeCaptainUser, 
                username='customer', 
                first_name='Customer',
                email='customer@customer.com', 
                uid = '2542c60b-54e0-4b0d-9d64-bac003967f93',
                salesforce_id = 'f7ef58fc-2702-48b1-96e2-1de7d58ad490'
            )
        self.customer = mommy.make(Customer, user=self.customer_user)

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
        
        self.agenda = mommy.make(
                                Event, property=self.r_property, 
                                buyer=self.customer.user, 
                                requested_by=self.loan_officer.user,
                                is_seller_required = False,
                                is_seller_realtor_required = False,
                                is_buyer_required = False,
                                is_buyer_loan_officer_required = False,
                                is_buyer_realtor_required = False,
                                is_buyer_concierge_required = False,
                                is_service_provider_required = False,
                                )

    # def test_post_agenda(self):
    #     data = {
    #             'name': 'Property Showing',
    #             'note': 'Lake property open house',
    #             'location': 'location1',
    #             'is_seller_required': False,
    #             'is_seller_realtor_required': False,
    #             'is_buyer_required': False,
    #             'is_buyer_loan_officer_required': False,
    #             'is_buyer_realtor_required': False,
    #             'is_buyer_concierge_required': False,
    #             'is_service_provider_required': False,
    #             'proposed_start': '2019-2-14T15:30:30',
    #             'proposed_end': '2019-2-14T17:30:30',
    #             'emails': {},
    #             'requesting_user_type': 'realtor',
    #             'is_confirmed': False,
    #             'property': self.r_property.id,
    #             'buyer': self.customer.user.username,
    #             'requested_by': self.realtor.user.id,
    #             'additional_attendees': [
    #             ]
    #         }
    #     res = self.client.post('/api/loan-officer/agenda/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     data = {
    #             'name': '',
    #             'note': '',
    #             'location': '',
    #             'is_seller_required': False,
    #             'is_seller_realtor_required': False,
    #             'is_buyer_required': False,
    #             'is_buyer_loan_officer_required': False,
    #             'is_buyer_realtor_required': False,
    #             'is_buyer_concierge_required': False,
    #             'is_service_provider_required': False,
    #             'proposed_start': '2019-2-14T15:30',
    #             'proposed_end': '2019-2-14T17:30',
    #             'emails': {},
    #             'requesting_user_type': 'realtor',
    #             'is_confirmed': False,
    #             'property': 0,
    #             'buyer': '',
    #             'requested_by': 0,
    #             'additional_attendees': [
    #
    #             ]
    #         }
    #     res = self.client.post('/api/loan-officer/agenda/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_agenda(self):
        res = self.client.get('/api/loan-officer/agenda/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_agenda_extras(self):
        res = self.client.get('/api/loan-officer/agenda/extras/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_agenda_uid(self):
        res = self.client.get('/api/loan-officer/agenda/'+ str(self.agenda.uid) +'/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get('/api/loan-officer/agenda/XXX/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # def test_put_agenda_uid(self):
    #     data = {
    #             'name': 'Property Showing',
    #             'note': 'Lake property open house',
    #             'location': 'locatio2',
    #             'is_seller_required': False,
    #             'is_seller_realtor_required': False,
    #             'is_buyer_required': False,
    #             'is_buyer_loan_officer_required': False,
    #             'is_buyer_realtor_required': False,
    #             'is_buyer_concierge_required': False,
    #             'is_service_provider_required': False,
    #             'proposed_start': '2019-2-14T15:30:30',
    #             'proposed_end': '2019-2-14T17:30:30',
    #             'emails': {},
    #             'requesting_user_type': 'realtor',
    #             'is_confirmed': False,
    #             'property': self.r_property.id,
    #             'buyer': self.customer.user.username,
    #             'requested_by': self.realtor.user.id,
    #             'additional_attendees': [
    #                 self.concierge.user.username
    #             ]
    #         }
    #     res = self.client.put('/api/loan-officer/agenda/' + str(self.agenda.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    # def test_patch_agenda_uid(self):
    #     data = {
    #             'name': 'Property Showing',
    #             'note': 'Lake property open house',
    #             'location': 'locatio3',
    #             'is_seller_required': False,
    #             'is_seller_realtor_required': False,
    #             'is_buyer_required': False,
    #             'is_buyer_loan_officer_required': False,
    #             'is_buyer_realtor_required': False,
    #             'is_buyer_concierge_required': False,
    #             'is_service_provider_required': False,
    #             'proposed_start': '2019-2-14T15:30:30',
    #             'proposed_end': '2019-2-14T17:30:30',
    #             'emails': {},
    #             'requesting_user_type': 'realtor',
    #             'is_confirmed': False,
    #             'property': self.r_property.id,
    #             'buyer': self.customer.user.username,
    #             'requested_by': self.realtor.user.id,
    #             'additional_attendees': [
    #                 self.concierge.user.username
    #             ]
    #         }
    #     res = self.client.patch('/api/loan-officer/agenda/' + str(self.agenda.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_agenda_uid(self):
        res = self.client.delete('/api/loan-officer/agenda/' + str(self.agenda.uid) + '/')
        #TODO: verify why this returns 403
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)   

    def test_get_customer(self):
        res = self.client.get('/api/loan-officer/customer/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_customer_export_customer(self):
        res = self.client.get('/api/loan-officer/customer/export-customers/?uids=' + str(self.customer.uid))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_customer_stats(self):
        res = self.client.get('/api/loan-officer/customer/stats/', data={'page': 'dashboard'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_customer_uid(self):
        res = self.client.get('/api/loan-officer/customer/' + str(self.customer.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_customer_uid(self):
        data = {
                'milestones': '',
                'buyer_seller': '',
                'seller': True,
                'buyer': True,
                'languages_spoken': {},
                'user': {
                            'id': self.customer.user.id,
                            'uid': self.customer.user.uid,
                            'username': self.customer.user.username,
                            'first_name': self.customer.user.first_name,
                            'last_name': self.customer.user.last_name,
                            'description': self.customer.user.description,
                            'user_type': 'Buyer',
                            'email': self.customer.user.email,
                            'phone': self.customer.user.phone,
                            "address": {
                                "street":self.address.street,
                                "city": self.address.city,
                                "state": self.address.state,
                                "postalcode": self.address.postalcode,
                                "country": self.address.country
                            },
                        },
                'requirements': [
      
                ],
                'properties': [

                ]
                }
        res = self.client.put('/api/loan-officer/customer/' + str(self.customer.uid) + '/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_customer_uid(self):
        data = {
                'milestones': '',
                'buyer_seller': '',
                'seller': True,
                'buyer': True,
                'languages_spoken': {},
                'user': {
                            'id': self.customer.user.id,
                            'uid': self.customer.user.uid,
                            'username': self.customer.user.username,
                            'first_name': self.customer.user.first_name,
                            'last_name': self.customer.user.last_name,
                            'description': self.customer.user.description,
                            'user_type': 'Buyer',
                            'email': self.customer.user.email,
                            'phone': self.customer.user.phone,
                            "address": {
                                "street":self.address.street,
                                "city": self.address.city,
                                "state": self.address.state,
                                "postalcode": self.address.postalcode,
                                "country": self.address.country
                            },
                        },
                'requirements': [
      
                ],
                'properties': [

                ]
                }
        res = self.client.patch('/api/loan-officer/customer/' + str(self.customer.uid) + '/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_customer_uid_archive(self):
        res = self.client.post('/api/loan-officer/customer/' + str(self.customer.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_customer_uid_restore(self):
        res = self.client.post('/api/loan-officer/customer/' + str(self.customer.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_customer_uid_status_update(self):
        data = {
                'milestones': 'Escrow',
                'buyer_seller': '',
                'seller': True,
                'buyer': True,
                'languages_spoken': {},
                'user': {
                            'id': self.customer.user.id,
                            'uid': self.customer.user.uid,
                            'username': self.customer.user.username,
                            'first_name': self.customer.user.first_name,
                            'last_name': self.customer.user.last_name,
                            'description': self.customer.user.description,
                            'user_type': 'buyer',
                            'email': self.customer.user.email,
                            'phone': self.customer.user.phone,
                            "address": {
                                "street":self.address.street,
                                "city": self.address.city,
                                "state": self.address.state,
                                "postalcode": self.address.postalcode,
                                "country": self.address.country
                            },
                        },
                'requirements': [
      
                ],
                'properties': [

                ]
                }
        res = self.client.patch('/api/loan-officer/customer/' + str(self.customer.uid) + '/status-update/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    ##commenting this because there is no email atrtribute on lender model
    #def test_get_email_receiver_type(self):
    #    res = self.client.get('/api/loan-officer/email/lender/')
    #    self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    #def test_post_email_receiver_type(self):
    #    res = self.client.post('/api/loan-officer/email/lender/', {})
    #    # TODO: ask on how to test this.
    #    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    # # def test_get_profile(self):
    # #     res = self.client.get('/api/loan-officer/profile/')
    # #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_profile(self):
        data = {
                'id': self.loan_officer.id,
                'uid': self.loan_officer.uid,
                'user': self.loan_officer.user.id,
                'lender': self.lender.id,
                'discourage_count': 0,
                'recommend_count': 0
            }
        res = self.client.put('/api/loan-officer/profile/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_profile(self):
        data = {
                'id': self.loan_officer.id,
                'uid': self.loan_officer.uid,
                'user': self.loan_officer.user.id,
                'lender': self.lender.id,
                'discourage_count': 0,
                'recommend_count': 0
            }
        res = self.client.patch('/api/loan-officer/profile/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_concierge(self):
        res = self.client.get('/api/loan-officer/team/concierge/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_team_concierge_archived(self):
        res = self.client.get('/api/loan-officer/team/concierge/archived/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_team_concierge_export_concierges(self):
        res = self.client.get('/api/loan-officer/team/concierge/export-concierges/?uids=' + str(self.concierge.uid))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_team_concierge_stats(self):
        res = self.client.get('/api/loan-officer/team/concierge/stats/', data={'page': 'dashboard'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_concierge_uid(self):
        res = self.client.get('/api/loan-officer/team/concierge/' + str(self.concierge.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    # def test_put_team_concierge_uid(self):
    #     data = {
    #             'user': {},
    #             'id': self.concierge.id,
    #             'uid': self.concierge.uid,
    #         }
    #     res = self.client.put('/api/loan-officer/team/concierge/' + str(self.concierge.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_patch_team_concierge_uid(self):
    #     data = {
    #             'user': {},
    #             'id': self.concierge.id,
    #             'uid': self.concierge.uid,
    #         }
    #     res = self.client.patch('/api/loan-officer/team/concierge/' + str(self.concierge.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_concierge_uid_archive(self):
        res = self.client.post('/api/loan-officer/team/concierge/' + str(self.concierge.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_concierge_uid_restore(self):
        res = self.client.post('/api/loan-officer/team/concierge/' + str(self.concierge.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_concierge_uid_discourage(self):
        res = self.client.post('/api/loan-officer/team/concierge/' + str(self.concierge.uid) + '/discourage/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_post_team_concierge_uid_recommend(self):
        res = self.client.post('/api/loan-officer/team/concierge/' + str(self.concierge.uid) + '/recommend/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    


    def test_get_team_realtor(self):
        res = self.client.get('/api/loan-officer/team/realtor/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_realtor_archived(self):
        res = self.client.get('/api/loan-officer/team/realtor/archived/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_realtor_stats(self):
        res = self.client.get('/api/loan-officer/team/realtor/stats/', data={'page': 'dashboard'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_team_realtor_uid(self):
        res = self.client.get('/api/loan-officer/team/realtor/' + str(self.realtor.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    # def test_put_team_realtor_uid(self):
    #     data = {
    #             'user': {
    #                 'salesforce_id': '003c000001DPiWsAAL',
    #             },
    #             'broker': {
    #                 'address': {}
    #             },
    #             'work_history': 0,
    #             'velocify_milestone_id': 0,
    #             'titlee': 'Team Lead',
    #             'title': self.realtor.title,
    #             'record_type_id': self.realtor.record_type_id,
    #             'realtor_unresponsive_count': 0,
    #             'realtor_score': 0,
    #             'owner_id': self.realtor.owner_id,
    #             'number_of_current_leads': 0,
    #             'new_score': 0,
    #             'nar_status': self.realtor.owner_id,
    #             'low_realtor_rating_count_from_lo': 0,
    #             'low_realtor_rating_count_from_customer': 0,
    #             'losses': 0,
    #             'leads_sent': 0,
    #             'last_modified_date': self.realtor.last_modified_date,
    #             'high_realtor_rating_count_from_lo': 0,
    #             'high_realtor_rating_count_from_customer': 0,
    #             'do_not_sms': True,
    #             'deals_sent': 0,
    #             'created_date': self.realtor.created_date,
    #             'counties_served': self.realtor.counties_served,
    #             'comments_reviews': self.realtor.comments_reviews,
    #             'closings': 0,
    #             'closing_percentage': 0,
    #             'balcklisted': True,
    #             'average_customer_realtor_rating': 0,
    #             'approval_status': self.realtor.approval_status,
    #             'military_service': self.realtor.military_service,
    #             'account_lost_count': 0,
    #             'realtor_contact_mobile_phone': self.realtor.realtor_contact_mobile_phone,
    #             'realtor_contact_company_phone': self.realtor.realtor_contact_company_phone,
    #             'velocify_realtor_phone': self.realtor.velocify_realtor_phone,
    #             'agent_milestone_end_cycle': True,
    #             'realtor_nps': 0,
    #             'realtor_interests': self.realtor.realtor_interests,
    #             'realtor_status_start_date': self.realtor.realtor_status_start_date,
    #             'send_realtor_status_e_mail': True,
    #             'franchisee': True,
    #             'amount_paid': self.realtor.amount_paid,
    #             'simplesms_donotsms': True
    #             }
    #     res = self.client.put('/api/loan-officer/team/realtor/' + str(self.realtor.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_patch_team_realtor_uid(self):
    #     data = {
    #             'user': {
    #                 'salesforce_id': '003c000001DPiWsAAL',
    #             },
    #             'broker': {
    #                 'address': {}
    #             },
    #             'work_history': 0,
    #             'velocify_milestone_id': 0,
    #             'titlee': 'Team Lead',
    #             'title': self.realtor.title,
    #             'record_type_id': self.realtor.record_type_id,
    #             'realtor_unresponsive_count': 0,
    #             'realtor_score': 0,
    #             'owner_id': self.realtor.owner_id,
    #             'number_of_current_leads': 0,
    #             'new_score': 0,
    #             'nar_status': self.realtor.owner_id,
    #             'low_realtor_rating_count_from_lo': 0,
    #             'low_realtor_rating_count_from_customer': 0,
    #             'losses': 0,
    #             'leads_sent': 0,
    #             'last_modified_date': self.realtor.last_modified_date,
    #             'high_realtor_rating_count_from_lo': 0,
    #             'high_realtor_rating_count_from_customer': 0,
    #             'do_not_sms': True,
    #             'deals_sent': 0,
    #             'created_date': self.realtor.created_date,
    #             'counties_served': self.realtor.counties_served,
    #             'comments_reviews': self.realtor.comments_reviews,
    #             'closings': 0,
    #             'closing_percentage': 0,
    #             'balcklisted': True,
    #             'average_customer_realtor_rating': 0,
    #             'approval_status': self.realtor.approval_status,
    #             'military_service': self.realtor.military_service,
    #             'account_lost_count': 0,
    #             'realtor_contact_mobile_phone': self.realtor.realtor_contact_mobile_phone,
    #             'realtor_contact_company_phone': self.realtor.realtor_contact_company_phone,
    #             'velocify_realtor_phone': self.realtor.velocify_realtor_phone,
    #             'agent_milestone_end_cycle': True,
    #             'realtor_nps': 0,
    #             'realtor_interests': self.realtor.realtor_interests,
    #             'realtor_status_start_date': self.realtor.realtor_status_start_date,
    #             'send_realtor_status_e_mail': True,
    #             'franchisee': True,
    #             'amount_paid': self.realtor.amount_paid,
    #             'simplesms_donotsms': True
    #             }
    #     res = self.client.patch('/api/loan-officer/team/realtor/' + str(self.realtor.uid) + '/', data=data, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_archive(self):
        res = self.client.post('/api/loan-officer/team/realtor/' + str(self.realtor.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_restore(self):
        res = self.client.post('/api/loan-officer/team/realtor/' + str(self.realtor.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_discourage(self):
        res = self.client.post('/api/loan-officer/team/realtor/' + str(self.realtor.uid) + '/discourage/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_team_realtor_uid_recommend(self):
        res = self.client.post('/api/loan-officer/team/realtor/' + str(self.realtor.uid) + '/recommend/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    



    





