from django.urls import path, include

from .views import DateCreateAPIView, WaterIntakeRetrieveCreateUpdateAPIView

urlpatterns = [
    path("date/", DateCreateAPIView.as_view(), name="date"),
    path("water-intake/", WaterIntakeRetrieveCreateUpdateAPIView.as_view(), name="water=intake"),
]