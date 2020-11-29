import json, pprint
from uuid import uuid4

from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Requirement
from apps.util.serializers import HCWritableNestedModelSerializer
from apps.concierge.serializers import ConciergeSerializer
from apps.realtor.serializers import RealtorSerializer
from apps.lender.serializers import LoanOfficerSerializer
from apps.concierge.serializers import ConciergeSerializer

class RequirementSerializer(HCWritableNestedModelSerializer):

    loan_officer = LoanOfficerSerializer(required=False) #TODO: move to requirements_serializer
    realtor = RealtorSerializer(required=False) #TODO: move to requirements_serializer
    assigned_rep = serializers.CharField(max_length=64, required=False)
    
    class Meta:
        model = Requirement
        depth = 5
        fields = ('loan_officer', 'realtor', 'assigned_rep', 
                  'desired_city_1', 'desired_city_2', 'desired_city_3',
                  'desired_state_1', 'desired_state_2', 'desired_state_3')

    def create(self, validated_data):
        #print("RequirementSerializer::create::validated_data", validated_data)
        
        is_valid = True
        
        realtor_data = validated_data.pop('realtor')
        if realtor_data:
            realtor_serializer = RealtorSerializer(
                data = realtor_data,
                context={'request': self.context['request']})
            is_valid = is_valid and realtor_serializer.is_valid()
            
        loan_officer_data = validated_data.pop('loan_officer')
        if loan_officer_data:
            loan_officer_serializer = LoanOfficerSerializer(
                data = loan_officer_data,
                context={'request': self.context['request']})
            is_valid = is_valid and loan_officer_serializer.is_valid()

        assigned_rep = validated_data.pop('assigned_rep', None)
        if assigned_rep:
            concierge_serializer = ConciergeSerializer(
                data = {
                    'user': {
                        'first_name': assigned_rep,
                        'salesforce_id': str(uuid4()),
                    }
                },
                context={'request': self.context['request']}
            )
            is_valid = is_valid and concierge_serializer.is_valid()
            
        if is_valid:
            realtor = realtor_serializer.save()
            loan_officer = loan_officer_serializer.save()
            concierge = concierge_serializer.save()
            customer = validated_data.pop('customer')
            
            try:
                #FIXME: for now, only one requirement can exist for a customer
                requirement = Requirement.objects.get(customer=customer)
                #for later
                #requirement, created = Requirement.objects.get(
                #    realtor=realtor, customer__user=customer__user,
                #    loan_officer=loan_officer,
                #)
            except Requirement.DoesNotExist:
                requirement = Requirement.objects.create(
                    realtor=realtor, customer=customer, concierge = concierge,
                    loan_officer=loan_officer, **validated_data
                )
                
        
        return requirement


class RequirementRealtorOrLoanOfficerUpdateSerializer(HCWritableNestedModelSerializer):
    loan_officer = LoanOfficerSerializer(required=False)
    concierge = ConciergeSerializer(required=False)
    class Meta:
        model = Requirement
        fields = (
            'id', 'uid', 'customer_id',
            'desired_city_1', 'desired_city_2', 'desired_city_3',
            'desired_state_1', 'desired_state_2', 'desired_state_3',
            'desired_property_description', 'target_price_minimum', 'target_price_maximum',
            'square_feet', 'bedrooms', 'bathrooms', 'loan_officer', 'concierge'
        )
        read_only_fields = ('loan_officer', 'concierge')
        extra_kwargs = {'uid': {'read_only': False, 'required': True}}

    # def update(self, instance, validated_data):
    #     for field in validated_data:
    #         setattr(instance, field, validated_data[field])
    #     instance.save()
            
