from django.db import models

from auth_app.models import User

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plans")
    week_number = models.IntegerField()
    date_range = models.CharField(max_length=25) 
    year = models.IntegerField()
    meal_name = models.CharField(max_length=100)
    day = models.CharField(max_length=10)
    meal_type = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.meal_type} meal plan for {self.user} on {self.day} of {self.date_range}"