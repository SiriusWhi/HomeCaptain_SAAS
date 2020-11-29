from .realtor_authenticated_apitestcase import RealtorAuthenticatedAPITestCase

from rest_framework import status

from model_mommy import mommy

from apps.lender.models import LoanOfficer

class RealtorTeamLoanOfficerTests(RealtorAuthenticatedAPITestCase):
    def test_get_realtor_team_loan_officer(self):
        res = self.client.get('/api/realtor/team/loan-officer/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'],1)

    def test_get_realtor_team_loan_officer_stats(self):
        res = self.client.get('/api/realtor/team/loan-officer/stats/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['current_count'],1)

    def test_get_realtor_team_loan_officer_uid(self):
        res = self.client.get('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    #ERROR: The `.update()` method does not support writable nested fields by default. 
    # Write an explicit `.update()` method for serializer `apps.concierge.serializers.ConciergeSerializer`, or set `read_only=True` on nested serializer fields.
    # def test_patch_realtor_team_loan_officer_uid(self):
    #     loan_officer = self.client.get('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/').data
    #     res = self.client.patch('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/', data=loan_officer, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    #ERROR: The `.update()` method does not support writable nested fields by default. 
    # Write an explicit `.update()` method for serializer `apps.concierge.serializers.ConciergeSerializer`, or set `read_only=True` on nested serializer fields.
    # def test_put_realtor_team_loan_officer_uid(self):
    #     loan_officer = self.client.get('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/').data
    #     res = self.client.put('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/', data=loan_officer, format='json')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_realtor_team_loan_officer_uid_archive(self):
        res = self.client.post('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/archive/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        loan_officers = self.client.get('/api/realtor/team/loan-officer/')
        self.assertEqual(loan_officers.data['count'],0)

    def test_post_realtor_team_loan_officer_uid_restore(self):
        res = self.client.post('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/restore/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        loan_officers = self.client.get('/api/realtor/team/loan-officer/')
        self.assertEqual(loan_officers.data['count'],1)

    def test_post_realtor_team_loan_officer_uid_discourage(self):
        res = self.client.post('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/discourage/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_realtor_team_loan_officer_uid_recommend(self):
        res = self.client.post('/api/realtor/team/loan-officer/' + str(self.loan_officer.uid) + '/recommend/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)




