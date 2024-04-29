from rest_framework.views import APIView

from .models import Profile, NotificationPreferences
from .serializers import ProfileSerializer, NotificationPreferencesSerializer
from .mixins import UserAssociatedMixin
# class ProfileRetrieveCreateUpdateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)


#     def post(self, request):
#         user = request.user
#         request.data['user'] = user.id
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request):
#         user_profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(user_profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NotificationPreferencesRetrieveCreateUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         preferences = NotificationPreferences.objects.get(user=request.user)
#         serializer = NotificationPreferencesSerializer(preferences)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         user = request.user
#         request.data['user'] = user.id
#         serializer = NotificationPreferencesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request):
#         preferences = NotificationPreferences.objects.get(user=request.user)
#         serializer = NotificationPreferencesSerializer(preferences, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveCreateUpdateAPIView(APIView, UserAssociatedMixin):
    def get_instance(self):
        return Profile.objects.get(user=self.request.user)

    def get_serializer_class(self):
        return ProfileSerializer

class NotificationPreferencesRetrieveCreateUpdateView(APIView, UserAssociatedMixin):
    def get_instance(self):
        return NotificationPreferences.objects.get(user=self.request.user)

    def get_serializer_class(self):
        return NotificationPreferencesSerializer
