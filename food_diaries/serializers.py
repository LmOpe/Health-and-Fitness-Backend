from rest_framework import serializers

from profiles.mixins import UpdateSerializerMixin
from .models import  WaterIntake, Date, Exercise, Meal, CalorieLog
from fudhouse.utils import calculate_calorie, convert_lbs_to_kg, convert_ft_to_cm, calculate_requirements

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


class CalorieLogSerializer(serializers.ModelSerializer):
    calorie = serializers.SerializerMethodField(read_only=True)
    carbs = serializers.SerializerMethodField(read_only=True)
    protein = serializers.SerializerMethodField(read_only=True)
    fats = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = CalorieLog
        fields = '__all__'
        

    def create(self, validated_data):
        user = validated_data.pop('user')
        date = validated_data.pop('date')

        try:
            calorie, carbs, protein, fats = calculate_requirements(user)
        except Exception as e:
            raise LookupError(e) from e

        instance = CalorieLog.objects.create(
            user=user,
            date=date,
            calorie=calorie,
            carbs=carbs,
            protein=protein,
            fats=fats,
            **validated_data
        )
        return instance

    def get_calorie(self, obj):
        return obj.calorie

    def get_carbs(self, obj):
        return obj.carbs

    def get_protein(self, obj):
        return obj.protein

    def get_fats(self, obj):
        return obj.fats