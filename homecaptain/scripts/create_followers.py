from actstream.actions import follow, unfollow

from apps.customer.models import Customer
from apps.requirement.models import Requirement
#from apps.realtor.models import Realtor
#from apps.lender.models import LoanOfficer
#from apps.concierge.models import Concierge



for customer in Customer.objects.all():
    for requirement in customer.requirements.all():
        follow(requirement.customer.user, customer)
        #follow(requirement.customer.user, requirement)

        follow(requirement.realtor.user, customer)
        #follow(requirement.realtor.user, requirement)

        follow(requirement.loan_officer.user, customer)
        #follow(requirement.loan_officer.user, requirement)

        follow(requirement.concierge.user, customer)
        #follow(requirement.concierge.user, requirement)
