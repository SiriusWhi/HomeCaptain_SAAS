from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import permissions
    
from django.apps import apps
from django.db.models import FieldDoesNotExist

from apps.customer.models import Customer
from apps.realtor.serializers import RealtorSerializer
from apps.realtor.models import Realtor, Broker
from apps.requirement.models import Requirement
from apps.util.api import HCRecordCreateGenericViewSet, EmailSendGenericView
from apps.util.tasks import generic_send_raw_email
from apps.util.permissions import IsRealtor

class RealtorRecordCreate(HCRecordCreateGenericViewSet):
    permission_classes = (permissions.IsAuthenticated, IsRealtor, )
    serializer_class = RealtorSerializer
    queryset = Realtor.objects.all()

    def create(self, request, *args, **kwargs):
        response = []
        success = failure = None

        request_data = request.data
        if not isinstance(request_data, (list,)):
            request_data = [request_data, ]

        for record in request_data:
            sanitized_record = self._sanitize_record(record, Realtor)
            serializer = self.get_serializer(data = sanitized_record)
            if serializer.is_valid(): #raise_exception=True):
                self.perform_create(serializer)
                serializer_data = serializer.data
                serializer_data['salesforce_id'] = serializer_data['user']['salesforce_id']
                response.append(serializer_data)
                success = True
            else:
                response.append({
                    'errors': serializer.errors,
                    'salesforce_id': sanitized_record.get('user').get('salesforce_id'),
                })
                failure = True
        if success and failure:
            http_status = status.HTTP_207_MULTI_STATUS
        elif success:
            http_status  = status.HTTP_201_CREATED
        else:
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(response, status=http_status)

class SendRealtorEmailView(EmailSendGenericView):
    sender_type = 'realtor'
    permission_classes = [permissions.IsAuthenticated, IsRealtor,]

    

@api_view(['GET', 'POST',])
@permission_classes([permissions.IsAuthenticated, IsRealtor,])
def recommend_us(request):
    if request.method == 'POST':
        receiver_user_email = request.data['email']
        user_type = request.data['user_type']
        
        ##commented for now
        ##FIXME: do we need more secuirty check here? like ->
        ##if realtor.is_attached_to_customer(customer):
        
        subject = "HomeCaptain recommendation"
        body = '''Hi
        %s wants you to checkout https://homecaptain.com. He finds it a super cool place to find your next
        home or the best place to sell your current home''' % request.user.username

        generic_send_raw_email.delay(request.user.uid,
                                     receiver_user_email, subject, body, 'recommend-hc')
    return Response({
        'fields': ('email', 'user-type',),
        'method': 'POST'
        })
