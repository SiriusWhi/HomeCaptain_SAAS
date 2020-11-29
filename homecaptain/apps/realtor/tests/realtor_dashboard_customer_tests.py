from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy

from apps.customer.models import Customer

class RealtorDashboardCustomerTests(RealtorAuthenticatedAPITestCase):
    def test_get_realtor_dashboard_customer(self):
        res = self.client.get('/api/realtor/customer/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'],1)

    def test_get_realtor_dashboard_customer_stats(self):
        res = self.client.get('/api/realtor/customer/stats/?page=dashboard')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['counts']['all'],1)

    def test_get_realtor_dashboard_customer_uid(self):
        res = self.client.get('/api/realtor/customer/' + str(self.customer.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    #ERROR: property with listing key x already exists
    def test_patch_realtor_dashboard_customer_uid(self):
        customer = self.client.get('/api/realtor/customer/' + str(self.customer.uid) + '/').data
        res = self.client.patch('/api/realtor/customer/' + str(self.customer.uid) + '/', data=customer, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    #ERROR: property with listing key x already exists
    def test_put_realtor_dashboard_customer_uid(self):
        customer = self.client.get('/api/realtor/customer/' + str(self.customer.uid) + '/').data
        res = self.client.put('/api/realtor/customer/' + str(self.customer.uid) + '/', data=customer, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_realtor_dashboard_customer_uid_archive(self):
        res = self.client.post('/api/realtor/customer/' + str(self.customer.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customers = self.client.get('/api/realtor/customer/')
        self.assertEqual(customers.data['count'],0)

    def test_post_realtor_dashboard_customer_uid_restore(self):
        res = self.client.post('/api/realtor/customer/' + str(self.customer.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customers = self.client.get('/api/realtor/customer/')
        self.assertEqual(customers.data['count'],1)

    def test_patch_realtor_dashboard_customer_uid_status_update(self):
        data = {
        'milestones': 'Escrowed',
        'buyer_seller': '',
        'seller': True,
        'buyer': True,
        'languages_spoken': {},
        'user': {
                    'id': self.customer.user.id,
                    'uid': self.customer.uid,
                    'username': self.customer.user.username,
                    'first_name': self.customer.user.first_name,
                    'last_name': self.customer.user.last_name,
                    'user_type': 'buyer',
                    'email': self.customer.user.email,
                    'phone': self.customer.user.phone,
                    'address': None
                },
        'requirements': [

        ],
        'properties': [

        ]
        }
        res = self.client.patch('/api/realtor/customer/' + str(self.customer.uid) + '/status-update/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['milestones'], 'Escrowed')

