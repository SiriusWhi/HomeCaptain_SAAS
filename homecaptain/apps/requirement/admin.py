from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Requirement

class RequirementAdmin(SimpleHistoryAdmin):
    pass

admin.site.register(Requirement, RequirementAdmin)
