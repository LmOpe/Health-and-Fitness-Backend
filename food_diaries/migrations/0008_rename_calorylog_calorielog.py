# Generated by Django 4.2 on 2024-05-03 21:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("food_diaries", "0007_calorylog_delete_energyrequired_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CaloryLog",
            new_name="CalorieLog",
        ),
    ]
