# from django.db import models

# from apps.customer.models import Customer
# from apps.lender.models import LoanOfficer
# from apps.realtor.models import Realtor
# from apps.concierge.models import Concierge

# """
# Option1: I could have used a generic app like https://github.com/wildfish/django-star-ratings 
# and cutomized the Rating model in it

# Or 

# Option2: Created one Rating model with generic ForeignKeys 

# OR

# Option3: For easier queries and organization and finite user types, I can create separate 
# rating models for each combination
# """

# class AbstractRatingModel(HomeCaptainAbstractBaseModel):
#     rating = models.IntegerField(default=0)
#     comments = models.CharField(max_length=2048, blank=True)
    
#     class Meta:
#         abstract = True

# class RealtorLoanOfficerRating(AbstractRatingModel):
#     realtor = models.ForeignKey(Realtor)
#     loan_officer = models.ForeignKey(LoanOfficer)

# class RealtorHCRepRating(AbstractRatingModel):
#     realtor = models.ForeignKey(Realtor)
#     concierge = models.ForeignKey(Concierge)
    
# class LoanOfficerRealtorRating(AbstractRatingModel):
#     loan_officer = models.ForeignKey(LoanOfficer)
#     realtor = models.ForeignKey(Realtor)

# class LoanOfficerHCRepRating(AbstractRatingModel):
#     loan_officer = models.ForeignKey(LoanOfficer)
#     concierge = models.ForeignKey(Concierge)

# class CustomerLoanOfficerRating(AbstractRatingModel):
#     customer = models.ForeignKey(Customer)
#     loan_officer = models.ForeignKey(LoanOfficer)

# class CustomerRealtorRating(AbstractRatingModel):
#     customer = models.ForeignKey(Customer)
#     realtor = models.ForeignKey(Realtor)

# class CustomerHCRepRating(AbstractRatingModel):
#     customer = models.ForeignKey(Customer)
#     concierge = models.ForeignKey(Concierge)

# class HCRealtorFeedback(AbstractRatingModel):
#     hc_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     cs = models.CharField(max_length=256, blank=True)
#     responsiveness = models.CharField(max_length=64, blank=True, choices=(
#         ('active', 'active'),
#     ))
#     knowledge = models.CharField(max_length=64, blank=True, choices=(
#         ('good', 'good'),
#     ))

# class HCLoanOfficerFeedback(AbstractRatingModel):
#     hc_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     cs = models.CharField(max_length=256, blank=True)
#     responsiveness = models.CharField(max_length=64, blank=True, choices=(
#         ('active', 'active'),
#     ))
#     knowledge = models.CharField(max_length=64, blank=True, choices=(
#         ('good', 'good'),
#     ))

    
