from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy

class RealtorListingsTests(RealtorAuthenticatedAPITestCase):
    def test_get_realtor_listings(self):
        res = self.client.get('/api/realtor/listings/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_get_realtor_listings_archived(self):
        res = self.client.get('/api/realtor/listings/archived/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 0)

    def test_get_realtor_listings_favorite_filters(self):
        res = self.client.get('/api/realtor/listings/favorite-filters/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('has_showings' in res.data.keys(), True)

    def test_get_realtor_listings_filters(self):
        res = self.client.get('/api/realtor/listings/filters/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('cities' in res.data.keys(), True)

    def test_get_realtor_listings_uid(self):
        res = self.client.get('/api/realtor/listings/' + str(self.r_property.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['uid'], str(self.r_property.uid))

    def test_post_realtor_listings_uid_add_recommend(self):
        data = {
            'usernames': [
                self.customer.user.username,
                self.realtor.user.username
            ]
        }
        res = self.client.post('/api/realtor/listings/' + str(self.r_property.uid) + '/recommend/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['message'], 'Successfully recommend the property')

    def test_post_realtor_listings_uid_archive(self):
        res = self.client.post('/api/realtor/listings/' + str(self.r_property.uid) + '/archive/')
        archived = self.client.get('/api/realtor/listings/archived/').data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(archived['count'], 1)

    def test_post_realtor_listings_uid_restore(self):
        res = self.client.post('/api/realtor/listings/' + str(self.r_property.uid) + '/restore/')
        archived = self.client.get('/api/realtor/listings/archived/').data
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(archived['count'], 0)