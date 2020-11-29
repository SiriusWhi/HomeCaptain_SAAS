from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy

from apps.event.models import Event

class RealtorAgendaTests(RealtorAuthenticatedAPITestCase):
    
    def test_get_realtor_agenda(self):
        res = self.client.get('/api/realtor/agenda/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['requested_by'], self.realtor.user.id)

    def test_post_realtor_agenda(self):

        data = {
            'property': self.agenda.property.id,
            'name': 'Property Showing',
            'note': '',
            'location': self.agenda.location,
            'is_seller_required': False,
            'is_seller_realtor_required': False,
            'is_buyer_required': True,
            'is_buyer_loan_officer_required': False,
            'is_buyer_realtor_required': True,
            'is_buyer_concierge_required': False,
            'is_service_provider_required': False,
            'proposed_start': '2010-02-23T17:30',
            'proposed_end': '2010-02-23T18:30',
            'emails': self.agenda.emails,
            'requested_by': self.agenda.requested_by.id,
            'requesting_user_type': 'realtor',
            'is_confirmed': False,
            'additional_attendees': []
        }
        res = self.client.post('/api/realtor/agenda/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        count = Event.objects.all().count()
        self.assertEqual(count,2)

    def test_get_realtor_agenda_extras(self):
        res = self.client.get('/api/realtor/agenda/extras/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['buyers'][0], self.customer_user.username)
    
    def test_get_realtor_agenda_uid(self):
        res = self.client.get('/api/realtor/agenda/' + str(self.agenda.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['uid'], str(self.agenda.uid))

    def test_put_realtor_agenda_uid(self):
        data = {
            'property': self.agenda.property.id,
            'name': 'Property Showing',
            'note': '',
            'location': self.agenda.location,
            'is_seller_required': False,
            'is_seller_realtor_required': False,
            'is_buyer_required': False,
            'is_buyer_loan_officer_required': False,
            'is_buyer_realtor_required': True,
            'is_buyer_concierge_required': False,
            'is_service_provider_required': False,
            'proposed_start': '2010-02-23T17:30',
            'proposed_end': '2010-02-23T18:30',
            'emails': self.agenda.emails,
            'requested_by': self.agenda.requested_by.id,
            'requesting_user_type': 'realtor',
            'is_confirmed': False,
            'additional_attendees': []
        }
        res = self.client.put('/api/realtor/agenda/' + str(self.agenda.uid) + '/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['is_buyer_required'], False)

    def test_patch_realtor_agenda_uid(self):
        data = {
            'property': self.agenda.property.id,
            'name': 'Property Showing',
            'note': '',
            'location': self.agenda.location,
            'is_seller_required': False,
            'is_seller_realtor_required': False,
            'is_buyer_required': True,
            'is_buyer_loan_officer_required': False,
            'is_buyer_realtor_required': False,
            'is_buyer_concierge_required': False,
            'is_service_provider_required': False,
            'proposed_start': '2010-02-23T17:30',
            'proposed_end': '2010-02-23T18:30',
            'emails': self.agenda.emails,
            'requested_by': self.agenda.requested_by.id,
            'requesting_user_type': 'realtor',
            'is_confirmed': False,
            'additional_attendees': []
        }
        res = self.client.patch('/api/realtor/agenda/' + str(self.agenda.uid) + '/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['is_buyer_realtor_required'], False)