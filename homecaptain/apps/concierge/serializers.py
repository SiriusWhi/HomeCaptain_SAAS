from rest_framework import serializers

#from apps.hcauth.models import HomeCaptainUser
from apps.hcauth.serializers import UserSerializer
from apps.util.serializers import HCWritableNestedModelSerializer
from .models import Concierge

class ConciergeSerializer(HCWritableNestedModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = Concierge
        depth = 1
        fields = ('user', 'id', 'uid', 'discourage_count', 'recommend_count')
        read_only_fields = ('user', 'discourage_count', 'recommend_count')
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        ##TODO enable when we make that portal
        ##user_data['user_type'] = 'Concierge'
        user_serializer = UserSerializer(
            data = user_data,
            context={'request': self.context['request']})
        try:
            concierge = Concierge.objects.get(name__iexact=user_data['first_name'])
        except Concierge.DoesNotExist:
            if user_serializer.is_valid():
                user = user_serializer.save()
                concierge = Concierge(user=user, name=user_data['first_name'])
                concierge.save()
        return concierge

class ConciergeOnlySerializer(HCWritableNestedModelSerializer):

    class Meta:
        model = Concierge
        fields = ('id', 'uid', 'discourage_count', 'recommend_count')
        read_only_fields = ('discourage_count', 'recommend_count')
        
