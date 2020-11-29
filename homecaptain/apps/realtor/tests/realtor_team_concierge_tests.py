from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy

from apps.concierge.models import Concierge

class RealtorTeamConciergeTests(RealtorAuthenticatedAPITestCase):
    def test_get_realtor_team_concierge(self):
        res = self.client.get('/api/realtor/team/concierge/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'],1)

    def test_get_realtor_team_concierge_stats(self):
        res = self.client.get('/api/realtor/team/concierge/stats/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['current'],1)

    def test_get_realtor_team_concierge_uid(self):
        res = self.client.get('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    #ERROR: The `.update()` method does not support writable nested fields by default. 
    # Write an explicit `.update()` method for serializer `apps.concierge.serializers.ConciergeSerializer`, or set `read_only=True` on nested serializer fields.
    # def test_patch_realtor_team_concierge_uid(self):
    #     concierge = self.client.get('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/').data
    #     res = self.client.patch('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/', data=concierge, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    #ERROR: The `.update()` method does not support writable nested fields by default. 
    # Write an explicit `.update()` method for serializer `apps.concierge.serializers.ConciergeSerializer`, or set `read_only=True` on nested serializer fields.
    # def test_put_realtor_team_concierge_uid(self):
    #     concierge = self.client.get('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/').data
    #     res = self.client.put('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/', data=concierge, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_realtor_team_concierge_uid_archive(self):
        res = self.client.post('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        concierges = self.client.get('/api/realtor/team/concierge/')
        self.assertEqual(concierges.data['count'],0)

    def test_post_realtor_team_concierge_uid_restore(self):
        res = self.client.post('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        concierges = self.client.get('/api/realtor/team/concierge/')
        self.assertEqual(concierges.data['count'],1)

    def test_post_realtor_team_concierge_uid_discourage(self):
        res = self.client.post('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/discourage/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_realtor_team_concierge_uid_recommend(self):
        res = self.client.post('/api/realtor/team/concierge/' + str(self.concierge.uid) + '/recommend/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)




