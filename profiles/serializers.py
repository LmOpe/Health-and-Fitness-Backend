from datetime import datetime

from rest_framework import serializers

from .models import Profile, NotificationPreferences, WaterIntake, Date
from .mixins import UpdateSerializerMixin

class ProfileSerializer(UpdateSerializerMixin, serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%d-%m-%Y'])
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'nutritional_goal', 'sex', 'dob', 'weight',\
             'height', 'activity_level', 'weight_unit', 'height_unit', 'age']

    def get_age(self, obj):
        dob = obj.dob
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

class NotificationPreferencesSerializer(UpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        fields = '__all__'

class WaterIntakeSerializer(UpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = '__all__'

class DateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d-%m-%Y'])

    class Meta:
        model = Date
        fields = ['id', 'date']