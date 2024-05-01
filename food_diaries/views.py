from rest_framework.views import APIView, Response, status

from .models import WaterIntake, Date, Exercise
from .serializers import WaterIntakeSerializer, DateSerializer, ExerciseSerializer
from profiles.mixins import UserAssociatedMixin

class WaterIntakeRetrieveCreateUpdateAPIView(APIView, UserAssociatedMixin):
    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        request.data['date'] = self.getDate()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_instance(self):
        try:
            return WaterIntake.objects.get(user=self.request.user, date=self.getDate())
        except WaterIntake.DoesNotExist:
           return None

    def get_serializer_class(self):
        return WaterIntakeSerializer

class DateCreateAPIView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        obj, created = Date.objects.get_or_create(date=date)
        serializer = DateSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class ExerciseListRetrieveCreateUpdateDeleteAPIView(APIView, UserAssociatedMixin):
    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        request.data['date'] = self.getDate()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        query_set = self.get_instance()
        if query_set:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "Object with user or date Not found"}, status.HTTP_404_NOT_FOUND)

    def get_instance(self):
        try:
            if self.request.method == "PUT":
                return Exercise.objects.get(user=self.request.user, date=self.getDate(), name=self.request.data['name'])
            elif self.request.method == "DELETE":
                return Exercise.objects.get(user=self.request.user, date=self.getDate(), name=self.request.query_params['name'])
            return Exercise.objects.filter(user=self.request.user, date=self.getDate())
        except Exercise.DoesNotExist:
            return None

    def get_serializer_class(self):
        return ExerciseSerializer