from rest_framework.views import APIView, Response, status

from .models import WaterIntake, Date
from .serializers import WaterIntakeSerializer, DateSerializer
from profiles.mixins import UserAssociatedMixin

class WaterIntakeRetrieveCreateUpdateAPIView(APIView, UserAssociatedMixin):
    def getDate(self):
        date = None
        if self.request.method == "GET":
            date = self.request.query_params.get("date")
        else:
            date = self.request.data["date"]
        dateObj, created = Date.objects.get_or_create(date=date)
        return dateObj.id

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