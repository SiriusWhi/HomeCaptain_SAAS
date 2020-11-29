# coding: utf-8
from rest_framework import routers

from django.urls import path, include, re_path

from .api import (
    SendLoanOfficerEmailView,
)

from .views import (
  LoanOfficerProfileViewSet,
  LoanOfficerDashboardBuyingSellingViewSet,
  LoanOfficerDashboardEventSlotViewSet,
  LoanOfficerMyConciergeViewSet,
  LoanOfficerMyRealtorViewSet
)

app_name = 'lender'

router = routers.SimpleRouter()
router.register(r'customer', LoanOfficerDashboardBuyingSellingViewSet)
router.register(r'agenda', LoanOfficerDashboardEventSlotViewSet)
router.register(r'team/concierge', LoanOfficerMyConciergeViewSet)
router.register(r'team/realtor', LoanOfficerMyRealtorViewSet)
# router.register(r'agenda', RealtorDashboardEventSlotViewSet)

loan_officer_self_profile = LoanOfficerProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})

urlpatterns = [
    path('profile/', loan_officer_self_profile, name="loan-officer-self-profile"),
    re_path('email/(?P<receiver_type>realtor|customer|concierge|broker)/',
            SendLoanOfficerEmailView.as_view(), name="loan-officer-send-email"),
]

urlpatterns += router.urls
