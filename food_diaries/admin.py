from django.contrib import admin

from .models import Date, WaterIntake, Exercise

admin.site.register([Date, WaterIntake, Exercise])