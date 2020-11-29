import json
from django.dispatch import receiver

from django.db.models.signals import pre_save, post_save

from actstream import action
from simple_history.signals import (
    pre_create_historical_record,
    post_create_historical_record
)
from actstream.actions import follow

from apps.requirement.models import HistoricalRequirement, Requirement

@receiver(post_save, sender=Requirement)
def create_requirement_followers(sender, instance, created, **kwargs):
    follow(instance.customer.user, instance.customer)
    if hasattr(instance, 'realtor') and getattr(instance, 'realtor', None):
        follow(instance.realtor.user, instance.customer)
    if hasattr(instance, 'loan_officer') and getattr(instance, 'loan_officer', None):
        follow(instance.loan_officer.user, instance.customer)
    if hasattr(instance, 'concierge') and getattr(instance, 'concierge', None):
        follow(instance.concierge.user, instance.customer)


@receiver(post_create_historical_record)
def post_create_historical_requirement_record_callback(sender, **kwargs):
    if sender == HistoricalRequirement:
        history_qs = kwargs['instance'].history
        if history_qs.count()>1:
            #changed
            new_record, old_record = history_qs.order_by('-history_date')[:2]
            delta = new_record.diff_against(old_record)
            changes = []
            for change in delta.changes:
                if change.field == 'modified':
                    continue
                changes.append("updated '%s' to '%s'" % \
                               (change.field, change.new))
            changes = ", ".join(changes)
            if changes:
                action.send(new_record.history_user, verb='Changed',
                            target=new_record.instance.customer,
                            action_object=new_record.instance, changes=changes)
        else:
            #created
            #send notifications to followers about creation of a new customer/requirement
            pass
