from django.contrib.auth import get_user_model
from django.db import transaction
from django.apps import apps

from rest_framework import serializers

from apps.customer.models import Customer
from apps.hcauth.serializers import UserSerializer
from apps.realtor.serializers import RealtorSerializer
from apps.lender.serializers import LoanOfficerSerializer
from apps.requirement.serializers import (
    RequirementSerializer,
    RequirementRealtorOrLoanOfficerUpdateSerializer,
)
from apps.property.serializers import PropertyRealtorOrLoanOfficerUpdateSerializer
from apps.util.serializers import HCWritableNestedModelSerializer
from apps.util.models import Address

class CustomerSerializer(HCWritableNestedModelSerializer):

    user = UserSerializer(required=True) 
    requirements = RequirementSerializer(required=False, many=True)
    ##TODO: include properties after MLS integration
    #properties = PropertySerializer(required=False, many=True)

    """
    NOTE: DRF warns of nested serializers and nested model serializers are harder
    ##https://www.django-rest-framework.org/api-guide/validators/#updating-nested-serializers
    ##TODO: https://github.com/beda-software/drf-writable-nested
    ##https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations

    Our request from SF creates a bunch of entities from a single object.
    So the object has become highly nested.
    """
    
    class Meta:
        model = Customer
        depth = 5
        fields = ('__all__')

    @transaction.atomic
    def create(self, validated_data):
        #print("CustomerSerializer::create::validated_data", validated_data)

        user_data = validated_data.pop('user')
        user_data['user_type'] = user_data['buyer_seller']
        user_serializer = UserSerializer(data = user_data,
                                         context={'request': self.context['request']})
        is_valid = user_serializer.is_valid()
        
        requirement_data = validated_data.pop('requirements')[0]
        requirement_serializer = RequirementSerializer(data=requirement_data,
                                                       context={'request': self.context['request']})
        #, many=True)
        is_valid = requirement_serializer.is_valid()
        
        if is_valid:
            user = user_serializer.save()
            customer, created = Customer.objects.update_or_create(
                user=user, **validated_data)
            requirement = requirement_serializer.save(customer=customer)
            return customer

    # def update(self, instance, validated_data):
    #     ##https://www.django-rest-framework.org/api-guide/serializers/#writing-update-methods-for-nested-representations
    #     pass

class CustomerRealtorUpdateSerializer(HCWritableNestedModelSerializer):
    """
    Why another customer serializer?
    1) The above one is aimed at taking data from salesforce which sends in a big nested object
       and it has power to create objects nested at level 5. Too much power
    2) A lesser API like one from Realtor Dashboard does not need and must not have that much power
    3) Another side effect of using the above highly nested serialzer is that it validates all 
       objects too and raises uncessary errors
    I am willing to discuss this further, if required - Jai [ Dec 24, 2018 ]
    """
    user = UserSerializer(required=True, exclude=('salesforce_id',))
    requirements = RequirementRealtorOrLoanOfficerUpdateSerializer(required=False, many=True)
    properties = PropertyRealtorOrLoanOfficerUpdateSerializer(required=False, many=True)
    
    class Meta:
        model = Customer
        fields = ('uid', 'milestones', 'buyer_seller', 'seller', 'buyer', 'languages_spoken',
                  'user', 'requirements', 'properties', 'customer_favorite_count',
                  'favorite_properties', 'scheduled_showings', 'customer_update_history', 'update_request_type')
        read_only_fields = ('uid', 'user', 'scheduled_showings', 'customer_update_history', 'update_request_type')
        
    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context['request']

        ##TODO: to be depricated
        ## replaced by status_update on realtor dashboard viewset
        milestones = validated_data.get('milestones', None)
        if milestones:
            instance.milestones = milestones
            instance.close_update_request(milestones, user=request.user)
            
        languages_spoken = validated_data.get('languages_spoken', None)
        if languages_spoken:
            instance.languages_spoken = languages_spoken
        instance.save()
            
        requirements_data = validated_data.pop('requirements', None)
        properties_data = validated_data.pop('properties', None)
        ##DID NOT WORK
        # if requirements_data:
        #     requirements_serializer = RequirementRealtorOrLoanOfficerUpdateSerializer(
        #         data=requirements_data, many=True)
        #     if requirements_serializer.is_valid():
        #         requirements_serializer.save()
                
        """
        Problem: requirements is a list and drf is removing uid from all objects
        in validation. So there is no way to find which requirement instance
        out of the list has changed!

        Solved by adding this to the RequirementRealtorOrLoanOfficerUpdateSerializer
        `extra_kwargs = {'uid': {'read_only': False, 'required': True}}`
        """

        ##DID NOT WORK
        # if requirements_data:
        #     for requirement_data in requirements_data:
        #         requirement_data['customer_id'] = instance.id
        #         requirement_serializer = RequirementRealtorOrLoanOfficerUpdateSerializer(
        #             data=requirement_data)
        #         if requirement_serializer.is_valid(raise_exception=True):
        #             requirement_serializer.save()


        ##SINCE THE ABOVE TWO WAYS DID NOT WORK AND WE NEED TO MOVE FORWARD FAST
        ##USING AN EASIER BUT LIMITED APPROACH
        ##https://stackoverflow.com/questions/37240621/django-rest-framework-updating-nested-object
        REQUIREMENT_FIELDS = (
            'desired_city_1', 'desired_city_2', 'desired_city_3',
            'desired_state_1', 'desired_state_2', 'desired_state_3',
            'desired_property_description', 'target_price_minimum', 'target_price_maximum',
            'square_feet', 'bedrooms', 'bathrooms'
        )
        if requirements_data:
            RequirementModel = apps.get_model('requirement', 'Requirement')
            for requirement_data in requirements_data:
                try:
                    requirement = RequirementModel.objects.get(uid=requirement_data['uid'])
                    for field in REQUIREMENT_FIELDS:
                        if field in requirement_data:
                            if requirement_data.get(field, ''):
                                setattr(requirement, field, requirement_data[field])
                    requirement.save()
                except RequirementModel.DoesNotExist:
                    pass #we don't create new requirements here

        PROPERTY_FIELDS = (
            'target_price_maximum', 'target_price_minimum', 'square_feet', 'bedrooms', 'bathrooms'
        )
        if properties_data:
            PropertyModel = apps.get_model('property', 'Property')
            for property_data in properties_data:
                try:
                    properti = PropertyModel.objects.get(uid=property_data['uid'])
                    for field in PROPERTY_FIELDS:
                        if property_data.get(field, ''):
                            setattr(properti, field, property_data[field])
                    properti.save()
                except PropertyModel.DoesNotExist:
                    pass #we don't create new requirements here
        return instance

class CustomerHomeCalculatorSerializer(serializers.Serializer):
    location = serializers.CharField()
    bedrooms = serializers.IntegerField()
    bathrooms = serializers.IntegerField()
    square_feet = serializers.IntegerField()

class CustomerHomeCalculatorAddPropertySerializer(serializers.Serializer):
    unit_number=serializers.CharField()
    street=serializers.CharField()
    city=serializers.CharField()
    state=serializers.CharField()
    postalcode=serializers.CharField()
    bedrooms = serializers.IntegerField()
    bathrooms = serializers.IntegerField()
    square_feet = serializers.IntegerField()

class CustomerMortgageCalculatorSerializer(serializers.Serializer):
    home_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    down_payment = serializers.DecimalField(max_digits=8, decimal_places=2)
    loan_program_payments = serializers.IntegerField()
    yearly_interest_rate = serializers.DecimalField(max_digits=4, decimal_places=2)
    yearly_taxes = serializers.DecimalField(max_digits=8, decimal_places=2)
    yearly_insurance = serializers.DecimalField(max_digits=8, decimal_places=2)

class CustomerPortalSerializer(HCWritableNestedModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = Customer
        depth = 1
        fields = ('id', 'uid', 'user',  'discourage_count', 'recommend_count') 
        read_only_fields = ('id', 'uid', 'discourage_count', 'recommend_count', )
    
    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context['request']
        user_serializer = UserSerializer(instance.user, data = validated_data.pop('user'),
                                         context={'request': self.context['request']})
        if user_serializer.is_valid():
            user = user_serializer.save()
            Customer.objects.filter(user=user).update(**validated_data)
            return request.user.customer
 