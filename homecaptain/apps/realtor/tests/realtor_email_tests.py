from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy

class RealtorEmailTests(RealtorAuthenticatedAPITestCase):
    def test_get_realtor_email_receiver_type(self):
        res = self.client.get('/api/realtor/email/realtor/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_realtor_email_receiver_type(self):
        res = self.client.post('/api/realtor/email/realtor/', {})
        # TODO: ask on how to test this.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
