from django.contrib import admin

from .models import Realtor, Broker, RealtorCertification

admin.site.register(Broker)
admin.site.register(Realtor)
admin.site.register(RealtorCertification)