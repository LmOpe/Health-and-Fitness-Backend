from django.db import models

from auth_app.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.URLField(blank=True, null=True)
    nutritional_goal = models.CharField(max_length=50)
    sex = models.CharField(max_length=6)
    dob = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=50)
    weight_unit = models.CharField(max_length=3)
    height_unit = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.user.username}"s profile'