from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers

class UserAssociatedMixin:
    permission_classes = [IsAuthenticated]

    def get_instance(self):
        raise NotImplementedError("You must implement get_instance method.")

    def get_serializer_class(self):
        raise NotImplementedError("You must implement get_serializer_class method.")

    def get(self, request):
        instance = self.get_instance()
        if instance:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "Not found"}, status.HTTP_404_NOT_FOUND)

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
        if self.request.data["date"]:
            self.request.data.pop("date")
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateSerializerMixin(serializers.Serializer):
    def update(self, instance, validated_data):
        print("Got to the update")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance