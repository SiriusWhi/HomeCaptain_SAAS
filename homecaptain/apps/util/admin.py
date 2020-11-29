from django.contrib import admin

from .models import (
    Address, SMS,
    RealtorInterest, 
    SalesforceStatus,
    HCOutGoingEmail
)

class SalesforceStatusAdmin(admin.ModelAdmin):
    list_display = ('created', 'code', 'message', 'content')

admin.site.register(Address)
admin.site.register(SMS)
admin.site.register(SalesforceStatus, SalesforceStatusAdmin)
admin.site.register(HCOutGoingEmail)
