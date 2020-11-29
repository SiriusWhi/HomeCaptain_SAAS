import json
from django.dispatch import receiver

from django.db.models.signals import pre_save, post_save
from django.conf import settings

from actstream import action
from simple_history.signals import (
    pre_create_historical_record,
    post_create_historical_record
)
from actstream.actions import follow

from apps.hcauth.models import HomeCaptainUser
from apps.property.models import HistoricalProperty, Property

@receiver(post_save, sender=Property)
def create_requirement_followers(sender, instance, created, **kwargs):
    ##FIXME: DRY WITH REQUIREMENT LATER
    follow(instance.customer.user, instance.customer)
    if instance.realtor:
        #becuase MLS properties might not have a realtor
        follow(instance.realtor.user, instance.customer)
    if instance.loan_officer:
        #because MLS PROPERTIES will not have a loan officer or concierge
        follow(instance.loan_officer.user, instance.customer)
    if instance.concierge:
        follow(instance.concierge.user, instance.customer)

@receiver(post_create_historical_record)
def post_create_historical_property_record_callback(sender, **kwargs):
    ##FIXME: DRY WITH REQUIREMENT LATER
    if sender == HistoricalProperty:
        history_qs = kwargs['instance'].history
        if history_qs.count()>1:
            #changed
            new_record, old_record = history_qs.order_by('-history_date')[:2]
            
            acting_user = new_record.history_user
            if not acting_user:
                acting_user = HomeCaptainUser.objects.get(username=settings.SYSTEM_USERNAME)
                
            delta = new_record.diff_against(old_record)
            changes = []
            for change in delta.changes:
                if change.field == 'modified':
                    continue
                changes.append("updated '%s' to '%s'" % \
                               (change.field, change.new))
            changes = ", ".join(changes)
            if changes:
                action.send(acting_user, verb='Changed',
                            target=new_record.instance.customer,
                            action_object=new_record.instance, changes=changes)
        else:
            #created
            #send notifications to followers about creation of a new customer/requirement
            pass
