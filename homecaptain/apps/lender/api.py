from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, status, viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from apps.lender.serializers import LoanOfficerSerializer, LenderSerializer#, LenderAdminSerializer
from apps.lender.models import Lender, LoanOfficer, LenderAdmin
from apps.util.api import HCRecordCreateGenericViewSet, EmailSendGenericView
from apps.util.permissions import IsLoanOfficer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class LoanOfficerRecordCreate(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = LoanOfficerSerializer
    queryset = LoanOfficer.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        response = []
        success = failure = None
        for record in request.data:
            serializer = self.get_serializer(data = record)
            if serializer.is_valid(): #raise_exception=True)
                self.perform_create(serializer)
                response.append(serializer.data)
                success = True
            else:
                response.append({
                    'errors': serializer.errors,
                    'salesforce_id': serializer.data['salesforce_id'],
                })
                failure = True
        if success and failure:
            http_status = status.HTTP_207_MULTI_STATUS
        elif success:
            http_status  = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(response, status=http_status)


class SendLoanOfficerEmailView(EmailSendGenericView):
    sender_type = 'loan-officer'
    permission_classes = [permissions.IsAuthenticated, IsLoanOfficer,]

        
