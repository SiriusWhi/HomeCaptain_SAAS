from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from simple_history.admin import SimpleHistoryAdmin

from .models import (Customer,
                     CustomerUpdate,)

class CustomerAdmin(SimpleHistoryAdmin):
    pass
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerUpdate)
