# coding: utf-8
from rest_framework import routers
from django.urls import path
from django.conf.urls import url

from .views import (
    PropertyPhotoOnDemandView,
    GeocodingView,
)

app_name = 'property'

router = routers.SimpleRouter()
router.register(r'photo', PropertyPhotoOnDemandView)

urlpatterns = router.urls
urlpatterns = urlpatterns + [url(r'geocode', GeocodingView.as_view())]
