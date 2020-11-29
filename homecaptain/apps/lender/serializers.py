from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError

from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer

from apps.hcauth.serializers import UserSerializer
from apps.util.serializers import AddressSerializer, HCWritableNestedModelSerializer
from .models import Lender, LenderAdmin, LoanOfficer, LoanOfficer

class LenderSerializer(HCWritableNestedModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Lender
        depth = 1
        fields = ('__all__')
        extra_kwargs = { #hack to avoid serializer throwimg up before reaching create
            'salesforce_id': {'validators': []},
        }

    def create(self, validated_data):
        address_serializer = AddressSerializer(data = validated_data.pop('address'))
        if address_serializer.is_valid():
            address = address_serializer.save()
            salesforce_id=validated_data.pop('salesforce_id')
            try:
                lender = Lender.objects.get(salesforce_id=salesforce_id)
            except Lender.DoesNotExist:
                lender, created = Lender.objects.get_or_create(
                    address=address, salesforce_id=salesforce_id,
                    **validated_data)
            return lender

class LoanOfficerSerializer(HCWritableNestedModelSerializer):

    user = UserSerializer(required=True)
    lender = LenderSerializer(required=True)
    
    class Meta:
        model = LoanOfficer
        depth = 3
        fields = ('id', 'uid', 'user', 'lender', 'discourage_count', 'recommend_count') 
        read_only_fields = ('id', 'uid', 'discourage_count', 'recommend_count', )
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'Loan Officer'
        user_serializer = UserSerializer(data = user_data,
                                         context={'request': self.context['request']})
        is_valid = user_serializer.is_valid()
        
        lender_serializer = LenderSerializer(data = validated_data.pop('lender'))
        is_valid = is_valid and lender_serializer.is_valid()
        
        if is_valid:
            user = user_serializer.save()
            lender = lender_serializer.save()
            try:
                loan_officer = LoanOfficer.objects.get(user=user)
            except LoanOfficer.DoesNotExist:
                loan_officer, created = LoanOfficer.objects.get_or_create(
                    user=user, lender=lender, **validated_data)
            return loan_officer

class LoanOfficerPortalSerializer(HCWritableNestedModelSerializer):
    """
    Creating a new LO serializer and not using the LoanOfficerSerializer because that it very powerful
    nested create and is used in conjunction with Salesforce data sync and migration
    """
    user = UserSerializer(required=True)
    #I am not sure if loan officer, a child node of lender, should be able to edit parent
    #so it's not a required attribute in request and is a readonly in reponse
    lender = LenderSerializer(required=False)
    
    class Meta:
        model = LoanOfficer
        depth = 1
        fields = ('id', 'uid', 'user', 'lender', 'discourage_count', 'recommend_count') 
        read_only_fields = ('id', 'uid', 'lender', 'discourage_count', 'recommend_count', )
    
    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context['request']
        user_serializer = UserSerializer(instance.user, data = validated_data.pop('user'),
                                         context={'request': self.context['request']})
        if user_serializer.is_valid():
            user = user_serializer.save()
            loan_officer = LoanOfficer.objects.filter(user=user).update(**validated_data)
            return request.user.loan_officer
        


# class LenderAdminSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = LenderAdmin
#         fields = ('lender', 'user', 'sf_account_id')


