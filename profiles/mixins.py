from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class UserAssociatedMixin:
    permission_classes = [IsAuthenticated]

    def get_instance(self):
        raise NotImplementedError("You must implement get_instance method.")

    def get_serializer_class(self):
        raise NotImplementedError("You must implement get_serializer_class method.")

    def get(self, request):
        instance = self.get_instance()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        instance = self.get_instance()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
