from django.db import models

from profiles.models import User
from fudhouse.utils import date_formatter

class Date(models.Model):
    date = models.DateField(db_index=True, unique=True)

    def __str__(self):
        return f'{date_formatter(self.date)}'

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
                             related_name="water_intake", db_index=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, db_index=True)
    number_of_glass = models.IntegerField()
    water_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0.25)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date_waterintake')
        ]

    def __str__(self):
        return f"Water Intake on {self.date} for {self.user.username}"

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
                             related_name="exercises", db_index=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=20)
    time_spent = models.IntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date', 'name'], name='unique_user_date_name_exercise')
        ]
    
    def __str__(self):
        return f"{self.name} on {self.date} for {self.user}"