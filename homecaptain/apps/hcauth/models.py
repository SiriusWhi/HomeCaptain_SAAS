#https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#a-full-example
import hashlib
from uuid import uuid4
from itertools import groupby

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    UserManager, AbstractUser
)

from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from actstream.models import Action

from apps.util.models import HomeCaptainAbstractBaseModel, Address
from apps.util.mixins import AddressModelLinkMixin
from apps.util.picklists import USER_TYPE_CHOICES
from apps.util.utils import get_logger

def get_placeholder_salesforce_id():
    return str(uuid4())

class HomeCaptainUser(AbstractUser, HomeCaptainAbstractBaseModel,
                      AddressModelLinkMixin):

    alternate_email = models.EmailField(_('email address'), blank=True)
    first_name = models.CharField(_('first name'), max_length=30, db_index=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, db_index=True, blank=True)

    salutation = models.CharField(max_length=16, blank=True)
    salesforce_id = models.CharField(max_length=36, unique=True, default=get_placeholder_salesforce_id)
    salesforce_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=16, blank=True) #accomodating as per the data from prod
    mobile = models.CharField(max_length=16, blank=True) #accomodating as per the data from prod
    alternate_phone = models.CharField(max_length=16, blank=True) #accomodating as per the data from prod
    ##need to move pictures to S3
    picture = models.ImageField(upload_to='media/uploads/customer_profile_pics', blank=True)
    description = models.TextField(default='', blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)

    alert_for_new_notifications = models.BooleanField(default=True)
    alert_for_new_messages = models.BooleanField(default=True)
    send_newsletters = models.BooleanField(default=False)
    send_new_listings = models.BooleanField(default=False)
    
    user_type = models.CharField(max_length=16, blank=True, choices=USER_TYPE_CHOICES)

    is_mls_auto_created = models.BooleanField(default=False)
    
    objects = UserManager()

    logger = get_logger('HomeCaptainUser')
    
    def __str__(self):
        return f"{self.username}"
    
    def get_user_type(self):
        if getattr(self, 'user_type', None):
            return self.user_type
        elif hasattr(self, 'customer') and getattr(self, 'customer'):
            if self.customer.buyer_seller == 'Buyer':
                return 'Buyer'
            elif self.customer.buyer_seller == 'Both':
                return 'Customer'
            elif self.customer.buyer_seller == 'Seller':
                return 'Seller'
        elif hasattr(self, 'realtor') and getattr(self, 'realtor'):
            return 'Realtor'
        elif hasattr(self, 'loan_officer') and getattr(self, 'loan_officer'):
            return 'Loan Officer'
        return None

    @property
    def info(self):
        return {
            'uid': str(self.uid),
            'salesforce_id': self.salesforce_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_type': self.get_user_type(),
        }

    
    def _modify_email_for_debug(self, email):
        if settings.DEBUG and email.split('@'):
            return email.split('@')[0] + '@example.org'
        else:
            return email
    
    def save(self, *args, **kwargs):
        #sanitizing for SF moved to apps.util.api.HCRecordCreateGenericViewSet._sanitize_record
        #if settings.DEBUG:
        #    if getattr(self, 'email', None):
        #        setattr(self, 'email', self._modify_email_for_debug(getattr(self, 'email')))
        #    if kwargs.get('email', None):
        #        kwargs['email'] = self._modify_email_for_debug(kwargs['email'])
        return super(HomeCaptainUser, self).save(*args, **kwargs)

    @property
    def is_realtor(self):
        if hasattr(self, 'realtor') and getattr(self, 'realtor', None):
            return True
        return False

    @property
    def is_loan_officer(self):
        if hasattr(self, 'loan_officer') and getattr(self, 'loan_officer', None):
            return True
        return False

    def get_my_top_notifications(self, n=200):
        return Notification.objects.filter(channel_id=self.id)[:n]

    def get_my_top_conversations(self, n=200):
        messages = HCMessage.objects.filter(models.Q(from_user=self)|models.Q(to_user=self))
        conversations = {}
        
        ##FIXME: using itertools.groupby will be inefficient for large data
        ##Which for one user, doesn't seem to be a plausible case, but still,
        ##Can use a raw query?       
        #raw_query = """select * from (select conversation_id, from_user_id, to_user_id, message, is_read, created from hcauth_hcmessage order by created desc) as temp group by temp.conversation_id,id;"""
        #or something like
        #raw_query = """select * from (select id, conversation_id, from_user_id, to_user_id, message, is_read, created from hcauth_hcmessage order by created desc) as temp group by temp.conversation_id,temp.id,temp.from_user_id,temp.to_user_id,temp.message,temp.is_read,temp.created;"""
        for conversation_id, group in groupby(messages.order_by('-created').\
                                              order_by('conversation_id')[:n], \
                                              key=lambda x: x.conversation_id):
            group_messages_list = [m.message_json for m in group]
            first_message = group_messages_list[0]
            self.logger.debug("%s : %s" % (first_message['to_user']['uid'], str(self.uid)))
            other_user = first_message['from_user'] if first_message['to_user']['uid']==str(self.uid) else first_message['to_user']
            conversations[conversation_id] = {
                'conversation_id': conversation_id,
                'user': other_user,
                'messages': group_messages_list
            }
        return conversations
    
class HomeCaptainRecommend(HomeCaptainAbstractBaseModel):
    recommended_user = models.ForeignKey(HomeCaptainUser, on_delete=models.CASCADE,
                                         related_name='recommended_model')
    recommended_author = models.ForeignKey(HomeCaptainUser, on_delete=models.CASCADE,
                                           related_name='recommend_model')
    
    class Meta:
        unique_together = (("recommended_author", "recommended_user"),)


class Discourage(HomeCaptainAbstractBaseModel):
    discouraging_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                                  related_name='discourages_given')
    discouraging_object_id = models.PositiveIntegerField()
    discouraging_content_object = GenericForeignKey('discouraging_content_type',
                                                    'discouraging_object_id')

    discouraged_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                                 related_name='discourages_received')
    discouraged_object_id = models.PositiveIntegerField()
    discouraged_content_object = GenericForeignKey('discouraged_content_type',
                                                   'discouraged_object_id')

    rating = models.IntegerField(null=True, blank=True)
    #this should trigger notifications on_save
    users_discouraged_to = models.ManyToManyField(HomeCaptainUser, blank=True) #blank for admin
    #this should trigger emails on save
    emails = JSONField(encoder=DjangoJSONEncoder, blank=True) 
    comments = models.TextField(blank=True)
    is_public = models.BooleanField(default=False, null=True)
    
    class Meta:
        unique_together = (('discouraging_content_type', 'discouraging_object_id',
                            'discouraged_content_type', 'discouraged_object_id'),)
    
    def __str__(self):
        return f'{self.discouraging_content_object} - {self.discouraged_content_object}'

class Recommend(HomeCaptainAbstractBaseModel):
    recommending_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                                  related_name='recommendations_given')
    recommending_object_id = models.PositiveIntegerField()
    recommending_content_object = GenericForeignKey('recommending_content_type',
                                                    'recommending_object_id')

    recommended_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                                 related_name='recommendations_received')
    recommended_object_id = models.PositiveIntegerField()
    recommended_content_object = GenericForeignKey('recommended_content_type',
                                                   'recommended_object_id')

    rating = models.IntegerField(null=True, blank=True)
    #this should trigger notifications on_save
    users_recommended_to = models.ManyToManyField(HomeCaptainUser, blank=True) #blank for admin
    #this should trigger emails on save
    emails = JSONField(encoder=DjangoJSONEncoder, blank=True) 
    comments = models.TextField(blank=True)
    is_public = models.BooleanField(default=False, null=True)

    class Meta:
        unique_together = (('recommending_content_type', 'recommending_object_id',
                            'recommended_content_type', 'recommended_object_id'), )

    def __str__(self):
        return f'{self.recommending_content_object} - {self.recommended_content_object}'


class Archive(HomeCaptainAbstractBaseModel):
    archiving_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                               related_name='archives_done')
    archiving_object_id = models.PositiveIntegerField()
    archiving_content_object = GenericForeignKey('archiving_content_type', 'archiving_object_id')

    archived_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                              related_name='archives_received')
    archived_object_id = models.PositiveIntegerField()
    archived_content_object = GenericForeignKey('archived_content_type', 'archived_object_id')

    comments = models.TextField(blank=True)

    class Meta:
        unique_together = (('archiving_content_type', 'archiving_object_id',
                            'archived_content_type', 'archived_object_id'), )
        
    def __str__(self):
        return f'{self.archiving_content_object} - {self.archived_content_object}'


class Favorite(HomeCaptainAbstractBaseModel):
    favoriting_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                               related_name='favorites_done')
    favoriting_object_id = models.PositiveIntegerField()
    favoriting_content_object = GenericForeignKey('favoriting_content_type', 'favoriting_object_id')

    favorited_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                              related_name='favorites_received')
    favorited_object_id = models.PositiveIntegerField()
    favorited_content_object = GenericForeignKey('favorited_content_type', 'favorited_object_id')

    comments = models.TextField(blank=True)

    class Meta:
        unique_together = (('favoriting_content_type', 'favoriting_object_id',
                            'favorited_content_type', 'favorited_object_id'), )
        
    def __str__(self):
        return f'{self.favoriting_content_object} - {self.favorited_content_object}'
    
class Notification(HomeCaptainAbstractBaseModel):
    channel = models.ForeignKey(HomeCaptainUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Action, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.channel} - {self.notification_text} - {self.activity.target} - {self.is_read}'

    @property
    def notification_text(self):
        target = self.activity.target.user.username
        if self.activity.target.user == self.channel:
            target = "you"
        return "%s %s for %s" % (
            self.activity.actor.username,
            self.activity.data.get('changes', str(self.activity)) if self.activity.data else  '',
            target)

    @property
    def notification_json(self):
        return {
            'uid': str(self.uid),
            'type': 'notification',
            'message': self.notification_text,
            'is_read': self.is_read,
            'created': self.created.isoformat()
        }


class HCMessage(HomeCaptainAbstractBaseModel):
    from_user = models.ForeignKey(HomeCaptainUser, on_delete=models.CASCADE,
                                  related_name='sent_messages')
    to_user = models.ForeignKey(HomeCaptainUser, on_delete=models.CASCADE,
                                related_name='received_messages')
    ##FIXME: don't want to set blank=True, but can't find an option!
    ##since the default callable can't take arguments
    ##and without arguments it's not possible to make a unique key
    ##so using pre_save signals and instance method to fill this
    ##attribute just before save based on the sender and receiver uids
    conversation_id = models.CharField(max_length=128, blank=True)
    ##TODO: validate message html before saving
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.conversation_id} - {self.from_user} - {self.to_user} - {self.message}'

    def set_conversation_id(self):
        uids = [
            str(self.from_user.uid).encode(encoding='utf-8'),
            str(self.to_user.uid).encode(encoding='utf-8')
        ]
        uids.sort()
        self.conversation_id = hashlib.md5(b''.join(uids)).hexdigest()
    
    @property
    def message_json(self):
        return {
            'uid': str(self.uid),
            'conversation_id': self.conversation_id,
            'type': 'message',
            'message': self.message,
            'is_read': self.is_read,
            'from_user': self.from_user.info,
            'to_user': self.to_user.info,
            'created': self.created.isoformat()
        }
    
    
