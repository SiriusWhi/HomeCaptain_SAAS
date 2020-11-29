from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.hcauth.models import HomeCaptainUser
from apps.util.utils import create_export_xlsx, get_usernames_and_emails
from apps.util.serializers import HCWritableNestedModelSerializer
from .models import Event


class EventSerializer(HCWritableNestedModelSerializer):
    buyer_username = serializers.ReadOnlyField(source='buyer.username')
    additional_attendees_usernames = serializers.ReadOnlyField(
        source='get_additional_attendees_usernames')
    
    ##still giving ids and not usernames
    # additional_attendees_usernames = serializers.PrimaryKeyRelatedField(
    #     many=True, read_only=False,
    #     queryset=HomeCaptainUser.objects.values_list('username', flat=True),
    #     source='additional_attendees')
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('buyer_username', 'additional_attendees_usernames')

    # def validate_buyer(self, value):
    #     ##FIXME - not used by DRF in is_valid for some reason
    #     ##so had to write the validation in viewset create
    #     try:
    #         return HomeCaptainUser.objects.get(username=value)
    #     except:
    #         raise serializers.ValidationError("Incorrect Buyer UserName")

    def create(self, validated_data):
        request = self.context['request']
        validated_data['requested_by'] = request.user
        
        requesting_user_type = 'realtor' if request.user.is_realtor else 'buyer'
        validated_data['requesting_user_type'] = requesting_user_type

        ##Moving them to invites
        # if requesting_user_type == 'buyer':
        #     validated_data['is_buyer_confirmed'] = True
        # elif requesting_user_type == 'realtor':
        #     validated_data['is_buyer_realtor_confirmed'] = True

            
        return super(EventSerializer, self).create(validated_data)
        
# class EventSlotUpdateSerializer(HCWritableNestedModelSerializer):
#     loan_officer = LoanOfficerSerializer(required=False)
#     concierge = ConciergeSerializer(required=False)
#     realtor = RealtorSerializer(required=False)
#     address = AddressSerializer(required=False, allow_null=True)

#     class Meta:
#         model = Property
#         fields = (
#             'id', 'uid', 'customer_id', 'description',
#             'target_price_minimum', 'target_price_maximum', 'created', 'address',
#             'square_feet', 'bedrooms', 'bathrooms', 'loan_officer', 'concierge',
#             'realtor', 'favorite_count', 'archived', 'property_favorite_count',
#             'favoriting_buyers'
#         )
#         read_only_fields = ('loan_officer', 'concierge', 'realtor',
#                             'property_favorite_count', 'favoriting_buyers')
#         extra_kwargs = {'uid': {'read_only': False, 'required': True}}
