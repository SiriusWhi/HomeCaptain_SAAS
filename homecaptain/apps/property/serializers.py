from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Property, PropertyPhoto
from apps.util.serializers import HCWritableNestedModelSerializer, AddressSerializer
from apps.lender.serializers import LoanOfficerSerializer
from apps.concierge.serializers import ConciergeSerializer
from apps.realtor.serializers import RealtorSerializer

class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = (
            'uid', 'property', 'media_modification_timestamp',
            'media_caption', 'media_description',
        )

class PropertyPhotoOnDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ('s3_url',)
        
class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False, allow_null=True)
    class Meta:
        model = Property
        fields = ('__all__')

    def create(self, validated_data):
        customer_property, created = Property.objects.update_or_create(**validated_data)
        return customer_property

class PropertyRealtorOrLoanOfficerUpdateSerializer(HCWritableNestedModelSerializer):
    loan_officer = LoanOfficerSerializer(required=False)
    concierge = ConciergeSerializer(required=False)
    realtor = RealtorSerializer(required=False)
    address = AddressSerializer(required=False, allow_null=True)
    photos = PropertyPhotoSerializer(many=True)
    
    class Meta:
        model = Property
        fields = (
            'id', 'uid', 'customer_id',
            'loan_officer', 'concierge', 'realtor', 
            'listing_key', 'listing_description', 'modification_timestamp', 'property_type',
            'property_sub_type', 'address', 'listing_url', 'lead_routing_email', 'mls_number',
            'lot_size', 'listing_date', 'listing_title',             
            'target_price_minimum', 'target_price_maximum',
            'square_feet', 'bedrooms', 'bathrooms', 'favorite_count',
            'valuation', 'year_built', 'full_bathrooms', 'three_quarter_bathrooms',
            'half_bathrooms',
            'one_quarter_bathrooms', 'foreclosure_status', 'listing_participants',
            'brokerage', 'location',
            'open_houses', 'taxes', 'expenses', 'detailed_characteristics', 
            'property_favorite_count', 'favoriting_buyers', 'scheduled_showings',
            'photos', 'favorite_count', 'lat', 'lng'
        )
        ##TODO: lot of the above should be read only, which one's?
        read_only_fields = ('loan_officer', 'concierge', 'realtor', 'scheduled_showings',
                            'property_favorite_count', 'favoriting_buyers')
        extra_kwargs = {'uid': {'read_only': False, 'required': True}}

        
class PropertyGeocodingSerializer(serializers.Serializer):
    addresses = serializers.JSONField()
