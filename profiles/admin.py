from django.contrib import admin

from .models import Profile, NotificationPreferences, Date, WaterIntake

admin.site.register([Profile, Date, NotificationPreferences, WaterIntake])