from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError

from rest_framework import serializers

from apps.hcauth.serializers import UserSerializer
from apps.util.serializers import AddressSerializer, HCWritableNestedModelSerializer
from .models import Realtor, Broker, RealtorCertification

class BrokerSerializer(HCWritableNestedModelSerializer):
    address = AddressSerializer(required=True)

    class Meta:
        model = Broker
        depth = 3
        fields = ('__all__')
        extra_kwargs = { #hack to avoid serializer throwimg up before reaching create
            'company': {'validators': []},
        }

    def create(self, validated_data):
        address_serializer = AddressSerializer(data = validated_data.pop('address'))
        if address_serializer.is_valid():
            address = address_serializer.save()
            company = validated_data.pop('company')
            try:
                broker = Broker.objects.get(company=company)
            except Broker.DoesNotExist:
                broker, created = Broker.objects.get_or_create(
                    address=address, company=company,
                    **validated_data)
            return broker
                              

class RealtorSerializer(HCWritableNestedModelSerializer):
    user = UserSerializer(required=True)
    broker = BrokerSerializer(required=True)
    certification = serializers.SerializerMethodField()
    discourage_count = serializers.ReadOnlyField()
    recommend_count = serializers.ReadOnlyField()

    class Meta:
        model = Realtor
        depth = 3
        fields = ('__all__')

    def get_certification(self,obj):
        try:
            res = RealtorCertification.objects.get(realtor=obj)
            return {'year': res.year, 'name': res.name, 'certifying_body': res.certifying_body}
        except Exception as e:
            return None
        
    def create(self, validated_data):
        #print("RealtorSerializer::create::validated_data", validated_data)

        user_data = validated_data.pop('user')
        user_data['user_type'] = 'Realtor'
        user_serializer = UserSerializer(data = user_data,
                                         context={'request': self.context['request']})
        broker_serializer = BrokerSerializer(data = validated_data.pop('broker'))
        if user_serializer.is_valid() and broker_serializer.is_valid():
            user = user_serializer.save()
            broker = broker_serializer.save()

            try:
                realtor = Realtor.objects.get(user=user)
            except Realtor.DoesNotExist:
                realtor, created = Realtor.objects.get_or_create(
                    user=user, broker=broker, **validated_data)
            return realtor

class RealtorOnlySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Realtor
        depth = 1
        exclude = ('user', 'broker', 'created', 'modified',)
        read_only_fields = ('discourage_count', 'recommend_count')
        

class RealtorPortalSerializer(HCWritableNestedModelSerializer):
    """
    Creating a new Realtor serializer and not using the RealRealtorSerializertor because that it very powerful
    nested create and is used in conjunction with Salesforce data sync and migration
    """
    user = UserSerializer(required=True)
    
    class Meta:
        model = Realtor
        depth = 1
        fields = ('id', 'uid', 'user', 'discourage_count', 'recommend_count') 
        read_only_fields = ('id', 'uid','discourage_count', 'recommend_count', )
    
    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context['request']
        user_serializer = UserSerializer(instance.user, data = validated_data.pop('user'),
                                         context={'request': self.context['request']})
        if user_serializer.is_valid():
            user = user_serializer.save()
            realtor = Realtor.objects.filter(user=user).update(**validated_data)
            return request.user.realtor

    @transaction.atomic
    def create(self, instance, validated_data):
        request = self.context['request']
        user_serializer = UserSerializer(instance.user, data = validated_data.pop('user'),
                                        context={'request': self.context['request']})
        if user_serializer.is_valid():
            user = user_serializer.save()
            realtor = Realtor()
            realtor.user = user
            realtor.save()

class RealtorUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    discourage_count = serializers.ReadOnlyField()
    recommend_count = serializers.ReadOnlyField()

    class Meta:
        model = Realtor
        depth = 2
        fields = ('__all__')
        
    def create(self, validated_data):
        user_serializer = UserSerializer(data = validated_data.pop('user'),
                                         context={'request': self.context['request']})
        
        if user_serializer.is_valid():
            user = user_serializer.save()
            try:
                realtor = Realtor.objects.get(user=user)
            except Realtor.DoesNotExist:
                realtor, created = Realtor.objects.get_or_create(
                    user=user, **validated_data)
            return realtor
