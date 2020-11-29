import requests
from datetime import datetime, timedelta

from celery import task, shared_task
from lxml import etree

from django.conf import settings
from django.db.models import F

from apps.util.models import Address
from apps.hcauth.models import HomeCaptainUser
from apps.customer.models import Customer
from apps.realtor.models import Realtor, Broker
from .models import Property, PropertyPhoto
from .mls_parsing_utils import parse_feed_element

@task(name='parse-mls-feed')
def parse_feed_and_create_properties():
    filename = None
    if settings.DEBUG:
        filename = settings.SAMPLE_MLS_DATA_FILE
    else:
        ##download file from listhub and use that
        raise Exception('Not Implemented')

    if not filename:
        return
    
    Property.objects.filter().update(strike=F('strike')+1)

    i = 0
        
    for event, element in etree.iterparse(
            filename, tag="{http://rets.org/xsd/Syndication/2012-03}Listing"):

        i += 1

        if settings.COUNT_OF_MLS_PROPERTIES_TO_PARSE and i >= settings.COUNT_OF_MLS_PROPERTIES_TO_PARSE:
            break
        
        try:
            listing = parse_feed_element(element)
        except Exception as e: #eat all, don't hold the parse for one
            ##TODO: notify the devs here with an email and traceback
            pass

        if not listing:
            continue

        listing['strike'] = 0
        
        listing_key = listing.pop('listing_key')
        modification_timestamp = listing['modification_timestamp']
        
        try:
            properti = Property.objects.get(listing_key=listing_key)
            if properti.modification_timestamp and \
               properti.modification_timestamp <= modification_timestamp:
                #if the property exists and is not modified in latest feed, pass
                properti.strike = 0
                properti.save()
                continue
        except Property.DoesNotExist:
            lead_routing_email = listing['lead_routing_email']

            user, created = HomeCaptainUser.objects.get_or_create(username=listing_key)
            ##not adding email because we don't want to send out emails to these auto created MLS realtors
            ##email=lead_routing_email)
            if created:
                user.is_mls_auto_created = True
                user.save()
            
            customer, created = Customer.objects.get_or_create(user=user)
            
            realtors = Realtor.objects.filter(user__email=lead_routing_email)
            if not realtors.exists():
                realtor_user, created = HomeCaptainUser.objects.get_or_create(username=lead_routing_email)
                if created:
                    realtor_user.first_name = listing['listing_participants'][0]['first_name']
                    realtor_user.last_name = listing['listing_participants'][0]['last_name'],
                    realtor_user.phone = listing['listing_participants'][0]['office_phone'],
                    realtor_user.is_mls_auto_created = True
                    realtor_user.save()
                
                broker = None
                if listing.get('brokerage', None) and listing['brokerage'].get('name', None):
                    broker, created = Broker.objects.get_or_create(company=listing['brokerage']['name'])
                    if created:
                        broker.is_mls_auto_created = True
                        broker.save()
                        
                if not broker:
                    realtor, created = Realtor.objects.get_or_create(user=realtor_user)
                else:
                    realtor, created = Realtor.objects.get_or_create(user=realtor_user, broker = broker)
                    
                if created:
                    realtor.is_mls_auto_created = True
                    realtor.save()
            else:
                realtor = realtors.first()
                
            properti = Property.objects.create(listing_key=listing_key, customer=customer,
                                               realtor=realtor, is_mls_auto_created=True)
            
        address = listing.pop('address')
        if getattr(properti, 'address', None):
            Address.objects.filter(id=properti.address.id).update(**address)
        else:
            address = Address.objects.create(**address)
            properti.address = address
            
        properti.save()
            
        photos = listing.pop('photos', [])

        Property.objects.filter(listing_key=listing_key).update(**listing)

        """
        {
            "media_modification_timestamp": "2012-03-06T17:14:47-05:00",
            "media_url": "http://photos.listhub.com/listing123/1",
            "media_caption": "Awesome Kitchen",
            "media_description": "Kitchen was recently remodeled"
        },
        """
        for photo in photos:
            media_url = photo.pop('media_url', None)
            if media_url:
                property = PropertyPhoto.objects.update_or_create(
                    media_url = media_url, property=properti, defaults = photo)

    properties_to_be_deleted = Property.objects.filter(is_mls_auto_created=True, strike=3)
    ##delete related customers and users
    HomeCaptainUser.objects.filter(customer__properties__in=properties_to_be_deleted,
                                   is_mls_auto_created=True).delete()
    HomeCaptainUser.objects.filter(realtor__properties__in=properties_to_be_deleted,
                                   is_mls_auto_created=True).delete()
    ##delete properties
    properties_to_be_deleted.delete()
    
    ##Q: Should we create a list of realtors with name, emails to reach out to them?
