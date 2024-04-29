from django.urls import path, include

from .views import ProfileRetrieveCreateUpdateAPIView

urlpatterns = [
    path("", ProfileRetrieveCreateUpdateAPIView.as_view(), name="user-profile"),   
]