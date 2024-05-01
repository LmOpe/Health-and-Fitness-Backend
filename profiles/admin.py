from django.contrib import admin

from .models import Profile, NotificationPreferences

admin.site.register([Profile, NotificationPreferences])