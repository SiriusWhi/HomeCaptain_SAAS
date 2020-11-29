import json
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from actstream.models import Action, Follow, followers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.hcauth.models import Notification, HCMessage, HomeCaptainUser
from apps.util.utils import get_logger

@receiver(post_save, sender=Action)
def create_notifications(sender, instance, **kwargs):
    """
    an activity instance was saved
    the target is a customer
    find the followers of that customer
    for each follower we create a new notification
    """
    if instance.verb == "started following":
        return
    target_followers = followers(instance.target)
    for target_follower in target_followers:
        #activity follower is an instance of HomeCaptainUser
        if target_follower is instance.actor:
            ##don't create notification for the actor themselves
            continue
        notification = Notification.objects.create(
            channel_id=target_follower.id,
            activity=instance)

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        channel_name = "notifications_%s" % instance.channel.uid
        ##NOTE: can't use await here because we are not in a async context
        ##the only way to do this async is use a celery task
        async_to_sync(channel_layer.group_send)(channel_name, {
            "type": "hc.notification", 
            "message": instance.notification_json
        })

@receiver(pre_save, sender=HCMessage)
def set_conversation_id(sender, instance, **kwargs):
    instance.set_conversation_id()
    
@receiver(post_save, sender=HomeCaptainUser)
def create_dependents(sender, instance, created, **kwargs):
    from django.apps import apps
    logger = get_logger('HomeCaptainUser:create_dependents')
    logger.debug("%s : %s : %s" % (sender, instance, created))
    if instance.user_type in ['Buyer', 'Seller']:
        if not (hasattr(instance, 'customer') and getattr(instance, 'customer', None)):
            Customer = apps.get_model('customer', 'Customer')
            Customer.objects.create(user=instance)
    elif instance.user_type in ['Loan Officer']:
        if not (hasattr(instance, 'loan_officer') and getattr(instance, 'loan_officer', None)):
            Lender = apps.get_model('lender', 'Lender')
            lender = Lender.objects.create(name=instance.username)
            LoanOfficer = apps.get_model('lender', 'LoanOfficer')
            LoanOfficer.objects.create(lender = lender, user=instance)
    elif instance.user_type in ['Realtor']:
        if not (hasattr(instance, 'realtor') and getattr(instance, 'realtor', None)):
            Realtor = apps.get_model('realtor', 'Realtor')
            Realtor.objects.create(user=instance)
        
            
            
            
