from decimal import Decimal
from random import shuffle, randint

import names

from django.db.models import Q

from apps.customer.models import Customer
from apps.requirement.models import Requirement
from apps.concierge.models import Concierge
from apps.realtor.models import Realtor, Broker
from apps.lender.models import Lender, LoanOfficer
from apps.hcauth.models import HomeCaptainUser
from apps.util.models import Address
from apps.property.models import Property
from apps.util.picklists import SELLER_MILESTONES_CHOICES

realtors = list(Realtor.objects.filter(
    Q(user__first_name__istartswith='Lisa') |
    Q(user__first_name__istartswith='Sheena') |
    Q(user__first_name__istartswith='Debra')))

loan_officers = list(LoanOfficer.objects.filter(
    Q(user__first_name__istartswith='David') |
    Q(user__first_name__istartswith='Christine') |
    Q(user__first_name__istartswith='Kendra')))

concierges = list(Concierge.objects.filter(
    Q(user__first_name__istartswith='Monique') |
    Q(user__first_name__istartswith='Suzanne') |
    Q(user__first_name__istartswith='Cindy')))


for i in range(100):
    print(i)
    if i%2 == 0:
        name = names.get_first_name(gender='male')
    else:
        name = names.get_first_name(gender='female')
    user = {
        'first_name': name,
        'username': "%s.%s" % (name, i),
        'email': "%s.%s@example.org" % (name, i)
    }
    u = HomeCaptainUser.objects.create(**user)
    properti = {
        'target_price_minimum': Decimal(randint(300000, 400000)),
        'target_price_maximum': Decimal(randint(400000, 500000)),
        'bedrooms': randint(3,6),
        'bathrooms': randint(3,6),
        'square_feet': randint(5000, 8000),
    }
    address = {
        'street': "%s Jake street" % randint(200, 500),
    }
    property_address = {
        'street': "%s prop street" % randint(200, 500),
    }
    a = Address.objects.create(**address)
    pa = Address.objects.create(**property_address)
    u.address = a
    u.save()
    shuffle(SELLER_MILESTONES_CHOICES)
    c = Customer(user=u, buyer_seller='Seller', seller=True,
                 milestones=SELLER_MILESTONES_CHOICES[0][0])
    c.save()
    shuffle(realtors)
    shuffle(concierges)
    shuffle(loan_officers)
    p = Property.objects.create(customer=c, address=pa,
                                concierge=concierges[0],
                                realtor = realtors[0],
                                loan_officer = loan_officers[0],
                                pre_qualification_amount=Decimal(123456),
                                valuation=Decimal(123456), **properti)
