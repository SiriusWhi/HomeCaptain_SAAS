from django.contrib import admin
from django.contrib.auth import admin as user_admin
from django.utils.translation import gettext, gettext_lazy as _

from .models import HomeCaptainUser, Notification, HCMessage, Recommend, Discourage, Archive


class HomeCaptainUserAdmin(user_admin.UserAdmin):
    readonly_fields = ('id', 'uid', 'salesforce_id')
    fieldsets = (
        (None, {'fields': ('id', 'uid', 'salesforce_id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Address'), {'fields': ('address',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    #fields = (
    #    'id', 'email', 'first_name', 'last_name', 'phone_number',
    #    'address_link', 'about', 'is_active', 'is_staff'
    #)

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ()
    filter_horizontal = ()

admin.site.register(HomeCaptainUser, HomeCaptainUserAdmin)
admin.site.register(Notification)
admin.site.register(HCMessage)
admin.site.register(Recommend)
admin.site.register(Discourage)
admin.site.register(Archive)
