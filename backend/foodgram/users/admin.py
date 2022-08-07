from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'email')


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
