from django.urls import path, include

from .views import MealPlanCreateListAPIView, MealPlanUpdateDeleteAPIView

urlpatterns = [
    path("meals/", MealPlanCreateListAPIView.as_view(), name="meal-plan"),
    path("meals/<int:pk>/", MealPlanUpdateDeleteAPIView.as_view(), name="meal-plan-single"),
]