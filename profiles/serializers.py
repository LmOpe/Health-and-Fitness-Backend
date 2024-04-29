from datetime import datetime

from rest_framework import serializers

from .models import Profile, NotificationPreferences

class ProfileSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(input_formats=['%d-%m-%Y'])
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'nutritional_goal', 'sex', 'dob', 'weight',\
             'height', 'activity_level', 'weight_unit', 'height_unit', 'age']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_age(self, obj):
        dob = obj.dob
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        fields = '__all__'
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance