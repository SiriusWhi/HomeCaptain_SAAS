from django.apps import apps
from django.conf import settings

from celery import task, shared_task

from apps.util.tasks import HCEmailMultiAlternatives

@task(name='send-event-invite-email')
def send_event_invites(sender_user_uid, receiver_emails, subject, body, template_name):
    User = apps.get_model('hcauth', 'HomeCaptainUser')
    sender = User.objects.get(uid=sender_user_uid)
    context = {"sender": sender}

    msg = HCEmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, receiver_emails,
                                   template_name=template_name, context=context)
    msg.send()
