from django.contrib import admin

from users.models import *

# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    """Admin view to display the call details of the calls made via exotel"""

    list_display = ('id', 'name', 'email')


admin.site.register(User, UsersAdmin)