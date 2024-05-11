from rest_framework.views import APIView, Response, status

from .models import Profile, NotificationPreferences
from .serializers import ProfileSerializer, NotificationPreferencesSerializer
from .mixins import UserAssociatedMixin

class ProfileRetrieveCreateUpdateAPIView(APIView, UserAssociatedMixin):
    def get_instance(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return None, Profile.__name__

    def get_serializer_class(self):
        return ProfileSerializer

class NotificationPreferencesRetrieveCreateUpdateView(APIView, UserAssociatedMixin):
    def get_instance(self):
        try:
            return NotificationPreferences.objects.get(user=self.request.user)
        except NotificationPreferences.DoesNotExist:
            return None, NotificationPreferences.__name__
    def get_serializer_class(self):
        return NotificationPreferencesSerializer