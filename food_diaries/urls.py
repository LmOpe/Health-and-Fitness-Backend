from django.urls import path, include

from .views import DateCreateAPIView, WaterIntakeRetrieveCreateUpdateAPIView, \
    ExerciseListCreateUpdateDeleteAPIView, MealListCreateUpdateDeleteAPIView,\
    CalorieLogRetrieveCreateUpdateAPIView

urlpatterns = [
    path("date/", DateCreateAPIView.as_view(), name="date"),
    path("water-intake/", WaterIntakeRetrieveCreateUpdateAPIView.as_view(), name="water=intake"),
    path("exercise/", ExerciseListCreateUpdateDeleteAPIView.as_view(), name="exercise"),
    path("exercise/<int:id>/", ExerciseListCreateUpdateDeleteAPIView.as_view(), name="exercise_delete"),
    path("meal/", MealListCreateUpdateDeleteAPIView.as_view(), name="meal"),
    path("meal/<int:id>/", MealListCreateUpdateDeleteAPIView.as_view(), name="meal_delete"),
    path("calorie-log/", CalorieLogRetrieveCreateUpdateAPIView.as_view(), name="calorie_log"),
]