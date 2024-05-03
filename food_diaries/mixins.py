from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles.mixins import UserAssociatedMixin

from .models import Exercise, Meal
from .serializers import ExerciseSerializer, MealSerializer

class GenericListCreateUpdateDeleteAPIView(UserAssociatedMixin, APIView):
    model = None
    serializer_class = None

    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        request.data['date'] = self.get_date()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({"Error": f"{self.model.__name__} with the name already exists, kindly update its value instead."},\
                    status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = self.get_instance()
        if queryset:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "Object with user or date not found"}, status.HTTP_404_NOT_FOUND)

    def get_instance(self, param=None):
        try:
            if self.request.method == "PUT":
                return self.model.objects.get(user=self.request.user, date=self.get_date(), name=self.request.data['name'])
            elif self.request.method == "DELETE":
                return self.model.objects.get(id=param)
            return self.model.objects.filter(user=self.request.user, date=self.get_date())
        except self.model.DoesNotExist:
            return None, self.model.__name__
            
    def get_serializer_class(self):
        return self.serializer_class