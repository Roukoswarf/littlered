from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from nanoms.models import (UserProperties,
                           Building,
                           Account,
                           Group,
                           Resident,
                           Device)

class ExtraProperties(admin.StackedInline):
    """"""
    model = UserProperties
    can_delete = False

class UserAdmin(BaseUserAdmin):
    """"""
    inlines = (ExtraProperties, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Building)
admin.site.register(Account)
admin.site.register(Group)
admin.site.register(Resident)
admin.site.register(Device)
