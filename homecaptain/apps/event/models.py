from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.util.models import HomeCaptainAbstractBaseModel
from apps.hcauth.models import HomeCaptainUser
from apps.property.models import Property
from apps.requirement.models import Requirement
from apps.util.picklists import EVENT_CHOICES

from apps.event.tasks import send_event_invites


#class AdditionalEventAttendee(HomeCaptainAbstractBaseModel):
#    attendee = models.OneToOneField(on_delete=models.CASCADE, to=HomeCaptainUser)
#    confirmed = models.BooleanField()


class Event(HomeCaptainAbstractBaseModel):
    """
    TODO: event will need to create invites - a new model and then get confirmations
    """

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='events',
                                 null=True, blank=True)
    name = models.CharField(max_length=64, choices = EVENT_CHOICES, blank=True)

    note = models.TextField(blank=True)
    location = models.CharField(max_length=256, blank=True)
    
    is_seller_required = models.BooleanField(default=False)
    is_seller_realtor_required = models.BooleanField(default=False)

    is_buyer_required = models.BooleanField(default=False)
    is_buyer_loan_officer_required = models.BooleanField(default=False)
    is_buyer_realtor_required = models.BooleanField(default=False)
    is_buyer_concierge_required = models.BooleanField(default=False)

    is_service_provider_required = models.BooleanField(default=False)
    
    proposed_start = models.DateTimeField(null=True, blank=True)
    proposed_end = models.DateTimeField(null=True, blank=True)

    ##Moving them to Invite
    # is_seller_confirmed = models.BooleanField(default=False)
    # is_seller_realtor_confirmed = models.BooleanField(default=False)
    # is_buyer_confirmed = models.BooleanField(default=False)
    # is_buyer_loan_officer_confirmed = models.BooleanField(default=False)
    # is_buyer_realtor_confirmed = models.BooleanField(default=False)
    # is_buyer_concierge_confirmed = models.BooleanField(default=False)
    # is_service_provider_confirmed = models.BooleanField(default=False)

    buyer = models.ForeignKey(HomeCaptainUser, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='buyer_showings')
    additional_attendees = models.ManyToManyField(HomeCaptainUser, blank=True) #blank for admin
    emails = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True) 
    
    requested_by = models.ForeignKey(HomeCaptainUser, on_delete=models.CASCADE,
                                     null=True, blank=True, related_name='requested_events')
    requesting_user_type = models.CharField(max_length=16, default='realtor', choices = (
        ('buyer', 'buyer'),
        ('realtor', 'realtor')
    ))

    ##TODO: to be added later
    ##service_providers = M2M with service provider table
    
    is_confirmed = models.BooleanField(default=False)

    def get_additional_attendees_usernames(self):
        if self.additional_attendees.exists():
            return self.additional_attendees.values_list('username', flat=True)
    
    def get_serialized_event(self):
        result = {
            'uid': self.uid,
            'name': self.name,
            'note': self.note,
            'location': self.location,
            'proposed_start': self.proposed_start.isoformat() if self.proposed_start else '',
            'proposed_end': self.proposed_start.isoformat() if self.proposed_end else '',
        }
        # if self.property:
        #     result.update({
        #         'property': {
        #             'address': self.property.address,
        #             'uid': self.property.uid,
        #             'realtor': {
        #                 'first_name': self.property.realtor.user.first_name,
        #                 'uid': self.property.realtor.uid
        #             }
        #         }
        #     })

        if self.requested_by:
            result.update({
                'requesting_user': self.requested_by.info
            })

        return result

        
    def __str__(self):
        return f"{self.name} - {self.proposed_start} - ( %s )" % self.property.uid if self.property else ''

@receiver(post_save, sender=Event, dispatch_uid="send_invite_emails")
def send_emails(sender, instance, **kwargs):
    receivers = []
    if instance.is_seller_required:
        if instance.property is not None:
            receivers.append(instance.property.customer.user.email)
    if instance.is_buyer_required:
        if instance.buyer is not None:
            receivers.append(instance.buyer.email)
    if instance.is_seller_realtor_required:
        if instance.property.realtor is not None:
            receivers.append(instance.property.realtor.user.email)
    queryset_buyer_requirements = Requirement.objects.filter(customer__user=instance.buyer)
    if instance.is_buyer_realtor_required:
        if len(queryset_buyer_requirements) > 0: 
            receivers.append(queryset_buyer_requirements.first().realtor.user.email)
    if instance.is_buyer_concierge_required:
        if len(queryset_buyer_requirements) > 0:   
            receivers.append(queryset_buyer_requirements.first().concierge.user.email)
    if instance.is_buyer_loan_officer_required:
        if len(queryset_buyer_requirements) > 0:    
            receivers.append(queryset_buyer_requirements.first().loan_officer.user.email) 
   # TODO: add service providers when implemented in model.
    attendees = instance.additional_attendees.all()
    for attendee in attendees:
        receivers.append(attendee.email)

    #Dummy for testing
    subject = 'Invitation to event ' + instance.name
    body = 'Test agenda invite'
    if len(receivers)>0:
        send_event_invites.delay(instance.requested_by.uid, receivers,
                                 subject, body, 'event-invite')
