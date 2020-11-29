# coding: utf-8
from rest_framework import routers
from django.conf.urls import url
from django.urls import path, re_path

from apps.customer.api import (
    CustomerRecordCreate,
    SendCustomerEmailView,
    CustomerMakeOffer,
    CustomerAcceptOffer,
    CustomerPreApprove
)

from .views import (
  CustomerMyConciergeViewSet,
  CustomerMyLoanOfficerViewSet,
  CustomerMyRealtorViewSet,
  CustomerPropertyViewSet,
  CustomerProfileViewSet,
  CustomerHomeCalculatorView,
  CustomerHomeCalculatorAddPropertyView,
  CustomerMortgageCalculatorView,
  CustomerEventSlotViewSet
)

app_name = 'customer'

router = routers.SimpleRouter()
router.register(r'create', CustomerRecordCreate)
router.register(r'agenda', CustomerEventSlotViewSet)
router.register(r'team/concierge', CustomerMyConciergeViewSet)
router.register(r'listing', CustomerPropertyViewSet, basename='customer-listing')
router.register(r'team/loan-officer', CustomerMyLoanOfficerViewSet)
router.register(r'team/realtor', CustomerMyRealtorViewSet)
urlpatterns = router.urls
urlpatterns = urlpatterns + [url(r'home-calculator',CustomerHomeCalculatorView.as_view())]
urlpatterns = urlpatterns + [path('add-property-from-calculator',CustomerHomeCalculatorAddPropertyView.as_view())]
urlpatterns = urlpatterns + [path('mortgage-calculator', CustomerMortgageCalculatorView.as_view())]
urlpatterns = urlpatterns + [
    path('accept-offer/', CustomerAcceptOffer.as_view(), name='customer-accept-offer'),
    path('make-offer/', CustomerMakeOffer.as_view(), name='customer-make-offer'),
    path('pre-approve/', CustomerPreApprove.as_view(), name='customer-pre-approve'),

]
customer_self_profile = CustomerProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})

urlpatterns = urlpatterns + [
    path('profile/', customer_self_profile, name="customer-self-profile"),
    re_path('email/(?P<receiver_type>realtor|loan-officer|concierge)/',
            SendCustomerEmailView.as_view(), name="customer-send-email"),
]
