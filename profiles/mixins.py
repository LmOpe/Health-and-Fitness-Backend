from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers

from food_diaries.models import Date, CalorieLog
from fudhouse.utils import calculate_requirements

class UserAssociatedMixin:
    permission_classes = [IsAuthenticated]


    def get_instance(self):
        raise NotImplementedError("You must implement get_instance method.")


    def get_serializer_class(self):
        raise NotImplementedError("You must implement get_serializer_class method.")


    def get_date(self):
        date = None
        if self.request.method == "GET" or self.request.method == "DELETE":
            try:
                date = self.request.query_params["date"]
            except:
                return None
        else:
            date = self.request.data["date"]
        date_obj, created = Date.objects.get_or_create(date=date)
        return date_obj.id


    def get(self, request):
        try:
            instance, name = self.get_instance()
        except TypeError:
             instance = self.get_instance()
        if instance:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": f"{name.lower()} for user or date was not found"}, status.HTTP_404_NOT_FOUND)


    def delete(self, request, id):
        try:
            instance, name = self.get_instance(id)
        except TypeError:
             instance = self.get_instance(id)
        if instance:
            if request.user == instance.user:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Error": "You do not have permission to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": f"{name.lower()} with the id was not found"}, status.HTTP_404_NOT_FOUND)


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
        try:
            instance, name = self.get_instance()
        except TypeError:
             instance = self.get_instance()
        serializer_class = self.get_serializer_class()

        try:
            if self.request.data["date"]:
                self.request.data.pop("date")
        except KeyError:
            pass

        if instance:
            serializer = serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                if self.__class__.__name__ == "ProfileRetrieveCreateUpdateAPIView":
                    try:
                        date = datetime.today().date()
                        calorie_log = CalorieLog.objects.get(user=instance.user, date=Date.objects.get(date=date).id)
                        calorie, carbs, protein, fats = calculate_requirements(instance.user)
                        calorie_log.calorie = calorie
                        calorie_log.carbs = carbs
                        calorie_log.protein = protein
                        calorie_log.fats = fats
                        calorie_log.save()
                    except CalorieLog.DoesNotExist:
                        pass 
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": f"{name.lower()} for user or date was not found"}, status.HTTP_404_NOT_FOUND)


class UpdateSerializerMixin(serializers.Serializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance