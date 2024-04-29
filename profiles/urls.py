from django.urls import path, include

from .views import ProfileRetrieveCreateUpdateAPIView, \
    NotificationPreferencesRetrieveCreateUpdateView, DateCreateAPIView, \
    WaterIntakeRetrieveCreateUpdateAPIView

urlpatterns = [
    path("", ProfileRetrieveCreateUpdateAPIView.as_view(), name="user-profile"),
    path("notification-preferences/", NotificationPreferencesRetrieveCreateUpdateView.as_view(), name="user-notification"),
    path("date/", DateCreateAPIView.as_view(), name="date"),
    path("water-intake/", WaterIntakeRetrieveCreateUpdateAPIView.as_view(), name="water=intake"),
]