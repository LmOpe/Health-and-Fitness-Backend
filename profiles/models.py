from django.db import models

from auth_app.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, \
        primary_key=True, related_name='profile', db_index=True)
    avatar = models.URLField(blank=True, null=True, max_length=3000)
    nutritional_goal = models.CharField(max_length=50)
    sex = models.CharField(max_length=6)
    dob = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=50)
    weight_unit = models.CharField(max_length=3)
    height_unit = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.user.email}-{self.user.username}"s profile'


class NotificationPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, \
        primary_key=True, related_name="notification_preferences", db_index=True)
    meal_recommendation = models.BooleanField(default=True)
    water_intake_reminder = models.BooleanField(default=True)
    food_log_reminder = models.BooleanField(default=True)
    goal_reminder = models.BooleanField(default=True)
    healthy_eating_reminder = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.email}-{self.user.username}"s \
                notification preferences'