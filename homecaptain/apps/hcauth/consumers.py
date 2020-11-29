import json
import asyncio
from itertools import groupby

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from json import JSONDecodeError

from django.db.models import Q

from apps.hcauth.models import HomeCaptainUser
from apps.requirement.models import Requirement
from apps.property.models import Property
from .models import Notification, HCMessage

class NotifyConsumer(AsyncJsonWebsocketConsumer):
    NOTIFICATION = "notification"
    MESSAGE = "message"
    CONVERSATION = "conversation"
    BUYER ="Buyer"
    SELLER = "Seller"
    BOTH = "Both"
    CUSTOMER = "Customer"
    REALTOR = "Realtor"
    LOAN_OFFICER = "Loan Officer"
    CONCIERGE = "Concierge"
    MARK_READ = "mark-read"
    SYSTEM = "system"
    ERROR = "error"
    ACK = "ack"
    
    async def connect(self):
        """
        This is the security built in. 
        Consumer is only reached when there is an authenticated user in scope
        That is ensured by custom token authentication provided by token_auth.py
        and used by the asgi routing.py
        """
        user = self.scope['user']
        self.room_name = user.uid
        self.room_group_name = '%ss_%s' % (self.NOTIFICATION, self.room_name)

        # Join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

        #await self.send_json({
        #    'type': self.NOTIFICATION,
        #    'message': "Hi %s, the %s" % (user.username, user.get_user_type())
        #})
        notifications = await self.get_top_notifications(user)
        for notification in notifications:
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "hc.%s" % self.NOTIFICATION, 
                'message': notification.notification_json
            })

        ##FETCH CONVERSATIONS
        conversations = await self.get_top_conversations(user)
        for conversation in conversations:
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "hc.%s" % self.MESSAGE, 
                'message': {
                    "type" : self.CONVERSATION,
                    "conversation": conversations[conversation]
                }
            })

    @database_sync_to_async
    def get_top_notifications(self, user):
        return list(user.get_my_top_notifications())

    @database_sync_to_async
    def get_top_conversations(self, user):
        return user.get_my_top_conversations()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def validate_uid(self, uid):
        try:
            return HomeCaptainUser.objects.get(uid=uid)
        except HomeCaptainUser.DoesNotExist:
            return None
        
    @database_sync_to_async
    def can_communicate(self, receiver):
        """
        Rule of thumb: sender can send messages to anyone on their 
            team on requirement or property
        """
        sender = self.scope['user']
        sender_type = sender.get_user_type()
        is_allowed = None

        ##Optimization Note: can be make the following queries simpler and DRY?
        if sender_type == self.REALTOR:
            qs1 = Requirement.objects.filter(
                Q(realtor__user=sender),
                Q(loan_officer__user=receiver)|Q(concierge__user=receiver)|Q(customer__user=receiver))
            qs2 = Property.objects.filter(
                Q(realtor__user=sender),
                Q(loan_officer__user=receiver)|Q(concierge__user=receiver)|Q(customer__user=receiver))
        elif sender_type == self.LOAN_OFFICER:
            qs1 = Requirement.objects.filter(
                Q(loan_officer__user=sender),
                Q(realtor__user=receiver)|Q(concierge__user=receiver)|Q(customer__user=receiver))
            qs2 = Property.objects.filter(
                Q(loan_officer__user=sender),
                Q(realtor__user=receiver)|Q(concierge__user=receiver)|Q(customer__user=receiver))
        elif sender_type in [self.BUYER, self.SELLER, self.CUSTOMER, self.BOTH]:
            qs1 = Requirement.objects.filter(
                Q(customer__user=sender),
                Q(realtor__user=receiver)|Q(concierge__user=receiver)|Q(loan_officer__user=receiver))
            qs2 = Property.objects.filter(
                Q(customer__user=sender),
                Q(realtor__user=receiver)|Q(concierge__user=receiver)|Q(loan_officer__user=receiver))
        elif sender_type == self.CONCIERGE:
            #TO BE IMPLEMENTED
            pass
            
        is_allowed = qs1.exists() or qs2.exists()
        
        if is_allowed:
            return True

        return None

    
    ## Receive message from WebSocket
    async def receive_json(self, json_data):
        try:
            json_data = json.loads(json_data)
        except Exception:
            #catch all
            json_data = json.loads(json.dumps(json_data))
        json_type = json_data.get('type', '')
        entity_type = json_data.get('entity_type', '')
        if json_type == self.MESSAGE:
            await self.send_message(json_data)
        elif entity_type in [self.NOTIFICATION, self.CONVERSATION] and \
             json_type ==  self.MARK_READ and json_data.get('uid'):
            marked_read = False
            if entity_type == self.NOTIFICATION:
                marked_read = await self.notification_mark_read(json_data['uid'])
            elif entity_type == self.CONVERSATION:
                marked_read = await self.conversation_mark_read(json_data['uid'])
            await self.channel_layer.group_send(
                '%ss_%s' % (self.NOTIFICATION, self.scope['user'].uid),
                {
                    'type': 'hc.%s.%s' % (self.SYSTEM, self.NOTIFICATION),
                    'message': {
                        "type": "%s.%s" % (self.SYSTEM, self.MARK_READ) ,
                        "entity_type": entity_type,
                        "uid": json_data['uid'],
                        "status": marked_read
                    }
                })
        else:
            await self.channel_layer.group_send(
                '%ss_%s' % (self.NOTIFICATION, self.scope['user'].uid),
                {
                    'type': 'hc.%s.%s' % (self.SYSTEM, self.NOTIFICATION),
                    'message': {
                        "type": "%s.%s" % (self.SYSTEM, self.ERROR),
                        'status': False,
                        "message": "Can't recognize the message type"
                    }
                })
            

    @database_sync_to_async
    def notification_mark_read(self, uid):
        try:
            notification = Notification.objects.get(uid=uid, channel=self.scope['user'])
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False

    @database_sync_to_async
    def conversation_mark_read(self, uid):
        try:
            message = HCMessage.objects.filter(conversation_id=uid, to_user=self.scope['user'])\
                      .filter(is_read=False).update(is_read=True)
            return True
        except HCMessage.DoesNotExist:
            return False

    @database_sync_to_async
    def create_message(self, receiver, message):
        hcmessage = HCMessage.objects.create(from_user=self.scope['user'], to_user=receiver, message=message)
        return hcmessage

    async def send_message(self, json_data):
        to_uid = json_data['to_uid']

        ##Need to do 5 things here
        ##1 - if uid is valid
        receiver = await self.validate_uid(to_uid)
        can_user_communicate = await self.can_communicate(receiver)
        
        ##2 - if the current user in scope can send a message to the user with stated uid
        if receiver and can_user_communicate:
            ##Note: Not suppressing exceptions here

            ##3 - persist the message
            hcmessage = await self.create_message(receiver, json_data['message'])
            
            ##4 - send the message
            await self.channel_layer.group_send(
                '%ss_%s' % (self.NOTIFICATION, to_uid),
                {
                    'type': 'hc.%s' % self.NOTIFICATION,
                    'message': hcmessage.message_json
                })
            await self.channel_layer.group_send(
                '%ss_%s' % (self.NOTIFICATION, self.scope['user'].uid),
                {
                    'type': 'hc.%s.%s' % (self.SYSTEM, self.NOTIFICATION),
                    'message': {
                        "type" : "%s.%s" % (self.MESSAGE, self.ACK),
                        "status": True,
                        "message": hcmessage.message_json
                    }
                })

            ##5 - in connect method above, fetch conversations
            
        else:
            #if the user is not allowed to send a message, send a denial message to them
            await self.channel_layer.group_send(
                '%ss_%s' % (self.NOTIFICATION, self.scope['user'].uid),
                {
                    'type': 'hc.%s.%s' % (self.SYSTEM, self.NOTIFICATION),
                    'message': {
                        'type': '%s.%s' % (self.SYSTEM, self.ERROR),
                        'status': False,
                        "message": "You can't send message to that user. %s %s" % (receiver, can_user_communicate)
                    }
                })
            
        
    async def hc_notification(self, event):
        message = event['message']
        ##CAN ADD SOME EXTRA STUFF HERE, THAT PERTAINS TO NOTIFICATIONS ONLY
        await self.send_json(message)

    async def hc_system_notification(self, event):
        message = event['message']
        ##CAN ADD SOME EXTRA STUFF HERE, THAT PERTAINS TO SYSTEM NOTIFICATIONS ONLY
        await self.send_json(message)

    async def hc_message(self, event):
        message = event['message']
        ##CAN ADD SOME EXTRA STUFF HERE, THAT PERTAINS TO MESSAGES ONLY
        await self.send_json(message)

