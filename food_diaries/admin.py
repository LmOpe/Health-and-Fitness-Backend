from django.contrib import admin

from .models import Date, WaterIntake, Exercise, Meal

admin.site.register([Date, WaterIntake, Exercise, Meal])