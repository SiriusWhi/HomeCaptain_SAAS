from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy

from ..models import Realtor

class RealtorAPITests(RealtorAuthenticatedAPITestCase):

    def test_create_bad_request(self):
        request_data = {
            "user": {
                "username": "",
                "first_name": "",
                "last_name": "",
                "description":"",
                "email": "",
                "phone": "",
                "address": {
                    "street": "",
                    "city": "",
                    "state": "",
                    "postalcode": "",
                    "country": ""
                },
                "salesforce_id": ""
            },
            "broker": {
                "address": {
                    "street": "",
                    "city": "",
                    "state": "",
                    "postalcode": "",
                    "country": ""
                },
                "work_history": None,
                "website_1": "",
                "website_2": "",
                "website_3": "",
                "phone": "",
                "nar_status": "",
                "master_broker_agreement_signed": False,
                "first_name": "",
                "last_name": "",
                "email": "",
                "company": ""
            },
            "certification": {
                    "year": 0,
                    "name": "",
                    "certifying_body": ""
                    },
            "work_history": None,
            "velocify_milestone_id": None,
            "titlee": None,
            "title": "",
            "record_type_id": "",
            "realtor_unresponsive_count": None,
            "realtor_score": None,
            "owner_id": "",
            "number_of_current_leads": None,
            "new_score": None,
            "nar_status": "",
            "low_realtor_rating_count_from_lo": None,
            "low_realtor_rating_count_from_customer": None,
            "losses": None,
            "leads_sent": None,
            "last_modified_date": None,
            "high_realtor_rating_count_from_lo": None,
            "high_realtor_rating_count_from_customer": None,
            "franchisee": False,
            "do_not_sms": False,
            "deals_sent": None,
            "created_date": None,
            "counties_served": "",
            "comments_reviews": "",
            "closings": None,
            "closing_percentage": None,
            "balcklisted": False,
            "average_customer_realtor_rating": None,
            "approval_status": "",
            "military_service": "",
            "account_lost_count": None
        }
        url = '/api/realtor/create/'
        res = self.client.post(url, data=request_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        count = Realtor.objects.all().count()
        self.assertEqual(count,1)
    
    def test_create(self):
        user = mommy.prepare('HomeCaptainUser')
        broker = mommy.prepare('Broker')
        request_data = {
            "user": {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "description":"description",
                "email": user.email,
                "phone": user.phone,
                "address": {
                    "street": "",
                    "city": "",
                    "state": "",
                    "postalcode": "",
                    "country": ""
                },
                "salesforce_id": user.salesforce_id
            },
            "broker": {
                "address": {
                    "street": "",
                    "city": "",
                    "state": "",
                    "postalcode": "",
                    "country": ""
                },
                "work_history": None,
                "website_1": "",
                "website_2": "",
                "website_3": "",
                "phone": "",
                "nar_status": "",
                "master_broker_agreement_signed": False,
                "first_name": "",
                "last_name": "",
                "email": "",
                "company": broker.company
            },
            "certification": {
                    "year": 0,
                    "name": "",
                    "certifying_body": ""
                    },
            "work_history": None,
            "velocify_milestone_id": None,
            "titlee": None,
            "title": "",
            "record_type_id": "",
            "realtor_unresponsive_count": None,
            "realtor_score": None,
            "owner_id": "",
            "number_of_current_leads": None,
            "new_score": None,
            "nar_status": "",
            "low_realtor_rating_count_from_lo": None,
            "low_realtor_rating_count_from_customer": None,
            "losses": None,
            "leads_sent": None,
            "last_modified_date": None,
            "high_realtor_rating_count_from_lo": None,
            "high_realtor_rating_count_from_customer": None,
            "franchisee": False,
            "do_not_sms": False,
            "deals_sent": None,
            "created_date": None,
            "counties_served": "",
            "comments_reviews": "",
            "closings": None,
            "closing_percentage": None,
            "balcklisted": False,
            "average_customer_realtor_rating": None,
            "approval_status": "",
            "military_service": "",
            "account_lost_count": None
        }
        url = '/api/realtor/create/'
        res = self.client.post(url, data=request_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        count = Realtor.objects.all().count()
        self.assertEqual(count,2)