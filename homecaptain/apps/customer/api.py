from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, mixins, permissions

from apps.customer.serializers import CustomerSerializer
from apps.customer.models import Customer
from apps.util.api import HCRecordCreateGenericViewSet, EmailSendGenericView
from apps.util.permissions import IsCustomer

class CustomerRecordCreate(HCRecordCreateGenericViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    
    def create(self, request, *args, **kwargs):
        response = []
        success = failure = None

        request_data = request.data
        if not isinstance(request_data, (list,)):
            request_data = [request_data, ]

        for record in request_data:
            sanitized_record = self._sanitize_record(record, Customer)
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

class SendCustomerEmailView(EmailSendGenericView):
    sender_type = 'customer'
    permission_classes = [permissions.IsAuthenticated, IsCustomer,]


class CustomerMakeOffer(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomer,]

    def get(self, request):
         return Response({
            'method': 'POST'
        })

    def post(self, request):
        customer = request.user.customer
        if customer.buyer_seller == 'Seller':
            return Response(
                {
                    "message": "Buyer can only make an offer"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        customer.milestones = 'Customer Offer Submitted'
        customer.save()
        return Response({
            "message": "Successfully made an offer"
        })


class CustomerAcceptOffer(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomer,]

    def get(self, request):
         return Response({
            'method': 'POST'
        })

    def post(self, request):
        customer = request.user.customer
        if customer.buyer_seller == 'Buyer':
            return Response(
                {
                    "message": "Seller can only make an offer"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        customer.milestones = 'Purchase Offer Submitted'
        customer.save()
        return Response({
            "message": "Successfully accepted an offer"
        })


class CustomerPreApprove(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomer,]

    def get(self, request):
         return Response({
            'method': 'POST'
        })

    def post(self, request):
        customer = request.user.customer
        customer_update = customer.create_update_request(
            requested_by=request.user,
            request_type='Pre Qualification Request'
        )
        return Response({
            "message": "Successfully pre approved an offer"
        })
