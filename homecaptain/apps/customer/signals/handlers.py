#https://django-simple-history.readthedocs.io/en/2.6.0/advanced.html#using-signals
from django.dispatch import receiver
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from actstream import action
from simple_history.signals import (
    pre_create_historical_record,
    post_create_historical_record
)

from apps.customer.models import HistoricalCustomer, Customer

@receiver(post_create_historical_record)
def post_create_historical_record_callback(sender, **kwargs):
    #https://django-simple-history.readthedocs.io/en/2.6.0/advanced.html#history-diffing
    """
    kwargs has the following: 

    instance :    The source model instance being saved
    history_instance : The corresponding history record
    history_date : Datetime of the history record's creation
    history_change_reason : Freetext description of the reason for the change
    history_user : The user that instigated the change
    """
    if sender == HistoricalCustomer:
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
                            target=new_record.instance, changes=changes)
        else:
            #created
            #send notifications to followers about creation of a new customer/requirement
            pass

@receiver(post_save, sender=Customer)
def create_dependents(sender, instance, created, **kwargs):
    if created:
        if instance.user.user_type in ['Both', 'Buyer']:
            if not instance.requirements.exists():
                Requirement = apps.get_model('requirement', 'Requirement')
                Requirement.objects.create(customer=instance)
        elif instance.user.user_type in ['Both', 'Seller']:
            if not instance.properties.exists():
                Property = apps.get_model('property', 'Property')
                Property.objects.create(customer=instance)
            
            
            
