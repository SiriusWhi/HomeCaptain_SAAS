from django.conf import settings
from django.db import models
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html


class UserModelLinkMixin(object):
    def user_link(self):
        return format_html('%s <u><a target="_blank" href="%s">Change</a></u>' % (escape(self.user), reverse("admin:hcauth_homecaptainuser_change", args=(self.user.id,))))

    user_link.allow_tags = True
    user_link.short_description = "User" 

class AddressModelLinkMixin(object):
    def address_link(self):
        return format_html('%s <u><a target="_blank" href="%s">Change</a></u>' % (escape(self.address), reverse("admin:util_address_change", args=(self.address.id,))))

    address_link.allow_tags = True
    address_link.short_description = "Address" 
