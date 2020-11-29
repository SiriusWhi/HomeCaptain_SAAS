import uuid

from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

try:
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import (
        setup_user_email,
        send_email_confirmation
    )
    from allauth.utils import email_address_exists
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

from apps.util.serializers import AddressSerializer, HCWritableNestedModelSerializer
from apps.util.models import SMS
from apps.util.picklists import USER_TYPE_CHOICES, NON_HC_STAFF_USER_TYPES

from .forms import HCPasswordResetForm


UserModel = get_user_model()

def get_placeholder_salesforce_id():
    return str(uuid.uuid4())    

class UserSerializer(HCWritableNestedModelSerializer):
    username = serializers.CharField(max_length=255, required=False)   
    address = AddressSerializer(required=False, allow_null=True)
    ##FIXME: this might give a 500 on DB IntegrityError if a existing LO, Realtor, Lender is forced
    salesforce_id = serializers.CharField(
        max_length=36,
        required=False,
        default=get_placeholder_salesforce_id,
        validators=[UniqueValidator(queryset=UserModel.objects.exclude(customer=None))]
    )
    class Meta:
        model = UserModel
        depth = 1
        fields = ('id', 'uid', 'username', 'first_name', 'last_name', 'user_type', 'get_user_type',
                  'email', 'phone', 'address', 'salesforce_id', 'alternate_email', 'description',
                  'alert_for_new_notifications', 'alert_for_new_messages',
                  'send_newsletters', 'send_new_listings')
        read_only_fields = ('id', 'uid', 'get_user_type', )
        #extra_kwargs = { #hack to avoid serializer throwimg up before reaching create
        #    'salesforce_id': {'validators': []},
        #}

    
    def create(self, validated_data):
        if not validated_data.get('username', None):
            first_name = validated_data.get('first_name', 'fakeusername').replace(' ', '')
            validated_data['username'] = "%s.%s" % (
                first_name, (UserModel.objects.count() + 1) )

        email = validated_data.pop('email', '')
        if email and validated_data.get('user_type', None) in NON_HC_STAFF_USER_TYPES and \
           len( email.split('@') ) > 1:
            if email.split('@')[1].lower() in ['homecaptain.com', 'roostify.com']:
                #for non HC staff users with HC domain emails -> put their email in `alternate_email`
                validated_data['alternate_email'] = email

        ##FIXME: SINCE WE ARE GETTING HC STAFF EMAILS REPEATEDLY FOR SEVERAL USERS,
        ##WE CANNOT IMPOSE UNIQUE CONSTRAINT ON THE EMAIL FIELD AT DB LEVEL
        ##BECAUSE IF WE PUT abc@homecaptain.com for them - uniqueness cannot be imposed!
        ##if we put blank in email field for them - uniqueness cannot be imposed!
        #elif UserModel.objects.filter(email=email).exists():
        #    ##Note: This app level email uniqueness validataion for incoming SF data
        #    raise serializers.ValidationError(["A user is already registered with this e-mail address.",])
                
                
        address_data = validated_data.pop('address', None)
        salesforce_id=validated_data.pop('salesforce_id')
        try:
            user = UserModel.objects.get(salesforce_id=salesforce_id)
        except UserModel.DoesNotExist:
            user, created = UserModel.objects.get_or_create(
                salesforce_id=salesforce_id, **validated_data)
            
        if address_data:
            address_serializer = AddressSerializer(user.address, data = address_data)
            if address_serializer.is_valid():
                address = address_serializer.save()

        """
        allauth/account/utils.py - L283
        - send_email_confirmation(request, user, signup=False)
        allauth/account/adapter.py -L433
        - send_confirmation_mail(self, request, emailconfirmation, signup)
        
        but the above does not allow to choose email template
        if we need to differentiate between signup and auto signup template
        we will need to replace the below code with AnyMail's custom email sending code
        """
        request = self.context['request']
        send_email_confirmation(request, user, signup=False)
        message = "Hi %s, You are now signed up at HomeCaptain." % user.first_name
        message += "Please check your email to confirm your account and login" 
        if settings.SEND_SMS and user.phone:
            SMS.objects.create(message=message, to=user.phone, sent_to=user)
        return user

    
class HCPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = HCPasswordResetForm


class HCRegisterSerializer(RegisterSerializer):
    user_type = serializers.ChoiceField(required=True,
                                        choices=USER_TYPE_CHOICES)
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'user_type': self.validated_data.get('user_type', '')
        }

    def save(self, request):
        ##Note: Overriding this for now because allauth.account.adapter.DefaultAccountAdapter
        ##save_user method does not save any other field than username, password, email
        ##instead of overriding the account adapter and using that in save method of this serializer
        ##I am overriding the save and adding user_type manually
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        ##
        user.user_type = self.cleaned_data['user_type']
        user.save()
        ##
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user



