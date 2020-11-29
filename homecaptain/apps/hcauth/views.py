import json
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_auth.registration.views import (SocialLoginView,
                                          RegisterView,
                                          VerifyEmailView)
from rest_auth.views import PasswordResetView, LoginView

from .models import HCMessage
from .serializers import (HCPasswordResetSerializer,
                          HCRegisterSerializer)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH2_CALLBACK_URL
    client_class = OAuth2Client

class HCPasswordResetView(PasswordResetView):
    serializer_class = HCPasswordResetSerializer

    
class HCVerifyEmailView(VerifyEmailView):
    
    def post(self, request, *args, **kwargs):
        kwargs.update(request.data)
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)   
        user = confirmation.email_address.user
        return redirect("/")


class HCLoginView(LoginView):
    def get_response(self):
        data = {
            'key': self.token.key,
            'user': self.user.info
        }
        return Response(data, status=status.HTTP_200_OK)

    
class CurrentUserView(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, format=None):
        return Response(request.user.info)


class HCRegisterView(RegisterView):
    serializer_class = HCRegisterSerializer
    
    def get_response_data(self, user):
        return {
            'user': user.info,
            'key': user.auth_token.key
        }

##TODO: Remove this later, this is for just testing notifications functionality
def notifications(request):
    return render(request, 'hcauth/notifications.html', context={
        "scheme": "wss" if request.is_secure() else "ws"
    })
