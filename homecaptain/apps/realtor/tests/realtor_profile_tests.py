from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy


class RealtorProfileTests(RealtorAuthenticatedAPITestCase):
    def test_get_realtor_profile(self):
        res = self.client.get('/api/realtor/profile/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['uid'], self.realtor.uid)

    def test_put_realtor_profile(self):
         profile = self.client.get('/api/realtor/profile/').data
         profile['user']['email'] = 'realtorput@realtor.com'
         res = self.client.put('/api/realtor/profile/', data=profile, format='json')
         self.assertEqual(res.status_code, status.HTTP_200_OK)
         self.assertEqual(res.data['user']['email'], 'realtorput@realtor.com')

    def test_patch_realtor_profile(self):
        profile = self.client.get('/api/realtor/profile/').data
        profile['user']['email'] = 'realtorpatch@realtor.com'
        res = self.client.patch('/api/realtor/profile/', data=profile, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['user']['email'], 'realtorpatch@realtor.com')