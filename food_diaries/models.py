from django.db import models

from profiles.models import User
from fudhouse.utils import date_formatter

class Date(models.Model):
    date = models.DateField(db_index=True, unique=True)

    def __str__(self):
        return f'{date_formatter(self.date)}'

class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s", db_index=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} on {self.date} for {self.user}"

class WaterIntake(BaseModel):
    number_of_glass = models.IntegerField()
    water_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0.25)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date_waterintake')
        ]
class Exercise(BaseModel):
    name = models.CharField(max_length=20)
    time_spent = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date', 'name'], name='unique_user_date_name_exercise')
        ]

class Meal(BaseModel):
    name = models.CharField()
    servings = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)
    energy = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date', 'name'], name='unique_user_date_name_meal')
        ]

class CalorieLog(BaseModel):
    calorie = models.DecimalField(decimal_places=2, max_digits=8)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date', 'calorie'], name='unique_user_date_calorie_calorielog')
        ]