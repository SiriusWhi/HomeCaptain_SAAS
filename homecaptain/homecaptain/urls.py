import urllib

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path, re_path

from allauth.socialaccount.models import SocialApp

from apps.hcauth.views import GoogleLogin
from rest_framework_swagger.views import get_swagger_view
from django.contrib.auth import views


from apps.hcauth.views import notifications

schema_view = get_swagger_view(title='HomeCaptain API')


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    path('api/auth/', include('apps.hcauth.urls', namespace='auth-api')),
    path('api/customer/', include('apps.customer.urls', namespace='customer-api')),
    url(r'api/docs/', schema_view),
    path('api/loan-officer/', include('apps.lender.urls', namespace='loan-officer-api')),
    path('api/realtor/', include('apps.realtor.urls', namespace='realtor-api')),
    path('api/property/', include('apps.property.urls', namespace='property-api')),

    url(r'^anymail/', include('anymail.urls')),

    url(r'^notifications/$', notifications, name='notifications'),
    
    # Not including activity urls for now
    # https://django-activity-stream.readthedocs.io/en/latest/installation.html#basic-app-configuration
    # The activity urls are not required for basic usage but provide activity Feeds and handle following, unfollowing and querying of followers.
    #url('^activity/', include('actstream.urls')),    
    path('realtor/', TemplateView.as_view(template_name="rindex.html")),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    ##TEMPORARY VIEWS 
    path('', TemplateView.as_view(
        template_name="index.html",
        extra_context={
            'redirect_url': urllib.parse.quote_plus(settings.GOOGLE_OAUTH2_CALLBACK_URL),
            'oauth_access_token_url': settings.GOOGLE_CODE_TO_ACCESS_TOKEN_URL,
            'google_oauth_client_id': settings.GOOGLE_OAUTH_CLIENT_ID
        }
    )),
    
]

if settings.DEBUG:
    urlpatterns = urlpatterns \
                  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns = urlpatterns + static('/realtor/',
                                       document_root=settings.REALTOR_DIST_DIR)
    urlpatterns = urlpatterns + static('/', document_root=settings.DIST_DIR)

    
    
#                  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

