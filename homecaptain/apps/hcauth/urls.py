from django.contrib.auth import views
from django.views.generic import TemplateView, RedirectView
from django.urls import path, re_path
from django.conf.urls import url

##importing and adding the following view urls for more control
##a simple include will not do that
from rest_auth.views import (
    LogoutView, PasswordChangeView,
    PasswordResetConfirmView
)
#from rest_auth.registration.views import RegisterView

from .views import (GoogleLogin ,
                    HCPasswordResetView,
                    HCVerifyEmailView,
                    HCLoginView,
                    CurrentUserView,
                    HCRegisterView)

app_name = 'auth'

urlpatterns = [
    ##rest auth
    path('password/reset/', HCPasswordResetView.as_view(),
         name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('login/', HCLoginView.as_view(), name='rest_login'),
    path('user/', CurrentUserView.as_view(), name='current_user_details'),

    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password/change/', PasswordChangeView.as_view(),
        name='rest_password_change'),

    # Swagger Login
    url('^swaggerlogin/', views.LoginView.as_view(template_name='hcauth/login.html'), name='swagger_login'),

    ##registration
    path('registration/', HCRegisterView.as_view(), name='rest_register'),

    re_path(r'registration/account-confirm-email/(?P<key>[-:\w]+)',
            HCVerifyEmailView.as_view(), name='account_confirm_email'),

    ##custom views
    path(r'google/', GoogleLogin.as_view(), name='google_login'),

]

#django/contrib/auth/views.py
# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above
