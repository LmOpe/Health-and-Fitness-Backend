from django.contrib import admin

from .models import Date, WaterIntake

admin.site.register([Date, WaterIntake])