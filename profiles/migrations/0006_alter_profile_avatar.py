# Generated by Django 4.2 on 2024-08-07 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_remove_waterintake_date_remove_waterintake_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
    ]
