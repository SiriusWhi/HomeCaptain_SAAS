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
from apps.util.picklists import MILESTONES_CHOICES

properties = list(Property.objects.all())
requirements = list(Requirement.objects.filter(realtor__user__username='Sheena.7'))
buyers = []
for requirement in requirements:
    if(requirement.customer.buyer_seller == 'Buyer'):
        buyers.append(requirement.customer)
shuffle(properties)
buyer_cnt = len(buyers)
for i in range(10):
    rand_buyer_idx = randint(0, buyer_cnt - 1)
    properties[i].favorite_users.add(buyers[rand_buyer_idx].user)
    properties[i].save()
