from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from nanoms import models

class ExtraProperties(admin.StackedInline):
    """"""
    model = models.UserProperties
    can_delete = False

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """"""
    inlines = (ExtraProperties, )

@admin.register(models.Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('street_address',
                  'unit_no',
                  'city',
                  'postal_code',
                  'province',
                  'country',)

@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Resident)
class ResidentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    pass
