from rest_framework import serializers

from profiles.mixins import UpdateSerializerMixin
from .models import  WaterIntake, Date, Exercise

class WaterIntakeSerializer(UpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = '__all__'

class DateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d-%m-%Y'])

    class Meta:
        model = Date
        fields = ['id', 'date']

class ExerciseSerializer(UpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'