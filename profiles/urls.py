from django.urls import path, include

from .views import ProfileRetrieveCreateUpdateAPIView, NotificationPreferencesRetrieveCreateUpdateView

urlpatterns = [
    path("", ProfileRetrieveCreateUpdateAPIView.as_view(), name="user-profile"),
    path('notification-preferences/', NotificationPreferencesRetrieveCreateUpdateView.as_view(), name="user-notification"),
]