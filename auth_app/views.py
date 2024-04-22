from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response

from djoser.views import UserViewSet as DjoserUserViewSet

class CustomUserViewSet(DjoserUserViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)