import requests
import traceback
from datetime import datetime, timedelta

from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceError
from celery import task, shared_task

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
#from django.core.mail import EmailMultiAlternatives
from anymail.message import AnymailMessage
from django.conf import settings
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.template.loader import get_template

from .utils import get_logger
from .models import SMS, SalesforceStatus, HCOutGoingEmail

UserModel = get_user_model()

def create_salesforce_error(error):
    SalesforceStatus.objects.create(
        message=getattr(error, 'message', ''),
        code=getattr(error, 'code', ''),
        url=getattr(error, 'url', ''),
        status=getattr(error, 'status', ''),
        resource_name=getattr(error, 'resource_name', ''),
        content=getattr(error, 'content', '')
    )

def create_salesforce_session():
    try:
        session = requests.Session()
        sf = Salesforce(password = settings.SALESFORCE_PASSWORD,
                        username = settings.SALESFORCE_USERNAME,
                        session=session, domain=settings.SALESFORCE_DOMAIN,
                        security_token = settings.SALESFORCE_SECURITY_TOKEN)
        return sf
    except SalesforceError as error:
        create_salesforce_error(error)
        raise error

##I do not want to create a new connection to salesforce every 5 minutes
##It might be costly and I am not sure how will Salesforce behave with it
##So I using a global variable and creating a single instance at the very start
##of Django and keep the session alive.
##For DEBUG mode, the connection is made when required. (when sending an SMS)
salesforce_instance = None
if not settings.DEBUG:
    salesforce_instance = create_salesforce_session()

    
class HCEmailMultiAlternatives(AnymailMessage):
    logger = get_logger('HCEmailMultiAlternatives')
    hc_template_name = None
    hc_created_by = None
    
    def __init__(self, subject, body, from_email, receiver_emails, *args, **kwargs):
            
        context = {"message": body}
        context.update(kwargs.pop('context', {}))

        ##don't fail silently
        ##Assumption: None of the emails we are sending out from here will be without template
        ##FIXME: for now monkey patching two attributes to message - template_name and created_by to be
        ##consumed in emailbackend. Find a better way later!
        self.hc_template_name = kwargs.pop('template_name') 

        template_bare_path = 'email/' + self.hc_template_name
        
        text_template = get_template(template_bare_path + '.txt')
        text_body = text_template.render(context)

        self.hc_created_by = kwargs.pop('sender', None)

        super().__init__(subject, text_body, from_email, receiver_emails, *args, **kwargs)
        
        html_template = get_template(template_bare_path + '.html')
        html_body = html_template.render(context)
        self.attach_alternative(html_body, "text/html")

@task(name='system-email')
def system_email(receiver_email, subject, body, template_name, context={}):
    ##TODO: use a template here
    receiver_emails = [receiver_email, ]
    user = UserModel.objects.get(uid=context.pop('user_uid'))
    context['user'] = user
    msg = HCEmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL,
                                   receiver_emails, template_name=template_name,
                                   context=context)
    msg.send()

            
@task(name='generic-send-raw-email')
def generic_send_raw_email(sender_user_uid, receiver_emails, subject, body, template_name):
    ##TODO: use a template here
    if not isinstance(receiver_emails, list):
        receiver_emails = [receiver_emails, ]

    sender = UserModel.objects.get(uid=sender_user_uid)
    context = {"sender": sender}
        
    msg = HCEmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL,
                                   receiver_emails, template_name=template_name,
                                   context=context)
    msg.send()


@task(name='generic-send-email')
def generic_send_email(sender_user_uid, sender_type, receiver_user_uids, receiver_type,
                       subject, body, template_name):

    ##DO NOT REMOVE
    # def _get_sender_receiver_model(sender_receiver_type):
    #     model = None
    #     if sender_receiver_type == 'realtor':
    #         model = apps.get_model('realtor', 'Realtor')
    #     elif sender_receiver_type == 'loan-officer':
    #         model = apps.get_model('loan_officer', 'LoanOfficer')
    #     elif sender_receiver_type == 'customer':
    #         model = apps.get_model('customer', 'Customer')
    #     elif sender_receiver_type == 'concierge':
    #         model = apps.get_model('concierge', 'Concierge')
    #     return model

    ##DO NOT REMOVE
    # def _is_attached(sender_type, sender_user_uid, receiver_type, receiver_user_uid):
    #     SenderModel = _get_sender_receiver_model(sender_type)
    #     ReceiverModel = _get_sender_receiver_model(receiver_type)
    #     sender = SenderModel.objects.get(user__uid=sender_user_uid)
    #     receiver = ReceiverModel.objects.get(user__uid=receiver_user_uid)
        
    #     is_attached = None
        
    #     if receiver_type == 'customer':
    #         is_attached = sender.is_customer_attached(receiver)
    #     elif receiver_type == 'loan-officer':
    #         is_attached = sender.is_loan_officer_attached(receiver)
    #     elif receiver_type == 'concierge':
    #         is_attached = sender.is_concierge_attached(receiver)
    #     elif receiver_type == 'realtor':
    #         is_attached = sender.is_realtor_attached(receiver)
            
    #     return is_attached
    
    #don't want to end up with cross import and cyclic import so trying dynamic model import 
    User = apps.get_model('hcauth', 'HomeCaptainUser')
    
    #FIXME: Probably, add some sender receiver `connected` validation here ?    
    #sender_user = get_object_or_404(User, uid=sender_user_uid)
    #if not sender_user.is_staff:
    #    # validate email sending only if the sender is not an admin
    #    if not _is_attached(sender_type, sender_user_uid, receiver_type, receiver_user_uid):
    #        return False

    sender = UserModel.objects.get(uid=sender_user_uid)
    receiver_users = UserModel.objects.filter(uid__in=receiver_user_uids).all()
    for receiver_user in receiver_users:
        ##TODO: STORE / LOG ALL EMAILS HERE, with sender
                      
        receiver_emails = [receiver_user.email, ]
        context = {"sender": sender, 'receiver': receiver_user}
        msg = HCEmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL,
                                       receiver_emails, template_name=template_name,
                                       context=context)
        
        msg.send()

@task(name='generic-send-sms')
def generic_send_sms(to, message):
    try:
        if settings.DEBUG:
            ##For debug mode, the instance is create on demand.
            if not salesforce_instance:
                salesforce_instance = create_salesforce_session()
            #send to Patrick in DEBUG MODE
            salesforce_instance.Textey_SMS__c.create(
                {"Phone__c": "2089498412", "Message__c": message})
        else:
            salesforce_instance.Textey_SMS__c.create({"Phone__c": to, "Message__c": message})
        return True
    except SalesforceExpiredSession as error:
        ##Salesforce expceptions are caught and store in SalesforceStatus table
        ##Admins should keep an eye on it.
        create_salesforce_error(error)
        ##If the session expired, create again.
        salesforce_instance = create_salesforce_session()
        return False
    except SalesforceError as error:
        create_salesforce_error(error)
        return False
    

@task(name='send-batch-sms')
def sender_batch_sms():
    if settings.SEND_SMS:
        ##A mximum of 50 objects in every 3 minutes
        ##as suggested by Gurpreet
        for sms in SMS.objects.filter(sent=False).all()[:50]:
            if generic_send_sms(sms.to, sms.message):
                sms.sent = True
                sms.save()
            
