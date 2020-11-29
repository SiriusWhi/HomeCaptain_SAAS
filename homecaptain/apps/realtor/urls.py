# coding: utf-8
from rest_framework import routers

from django.urls import path, include, re_path

from .api import (
    RealtorRecordCreate,
    SendRealtorEmailView,
    # send_email,
    recommend_us
)    
from .views import (
    RealtorSelfProfileViewSet,
    RealtorDashboardCustomersViewSet,
    RealtorDashboardArchivedViewSet,
    RealtorPropertiesViewSet,
    RealtorDashboardMyLoanOfficerViewSet,
    RealtorDashboardMyConciergeViewSet,
    RealtorDashboardEventSlotViewSet
)

app_name = 'realtor'

router = routers.SimpleRouter()
router.register(r'create', RealtorRecordCreate)
router.register(r'customer', RealtorDashboardCustomersViewSet)
router.register(r'dashboard/archived', RealtorDashboardArchivedViewSet, basename='dashboard-archived')
router.register(r'listings', RealtorPropertiesViewSet)
router.register(r'team/loan-officer', RealtorDashboardMyLoanOfficerViewSet)
router.register(r'team/concierge', RealtorDashboardMyConciergeViewSet)
router.register(r'agenda', RealtorDashboardEventSlotViewSet)

realtor_self_profile = RealtorSelfProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})

urlpatterns = [
    path('recommend-us/', recommend_us, name='recommend-us'),
    path('profile/', realtor_self_profile, name="realtor_self_profile"),
    re_path('email/(?P<receiver_type>realtor|customer|loan-officer|concierge)/',
        SendRealtorEmailView.as_view() , name="realtor-send-email"),
    
]

urlpatterns += router.urls
