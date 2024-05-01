from rest_framework import serializers

from profiles.mixins import UpdateSerializerMixin
from .models import  WaterIntake, Date, Exercise, Meal

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

class MealSerializer(UpdateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'