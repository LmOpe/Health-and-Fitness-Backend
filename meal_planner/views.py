from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import MealPlan
from .serializers import MealPlanSerializer


class MealPlanCreateListAPIView(APIView):
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = MealPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def get(self, request):
        meal_plans = None
        try:
            date_range = self.request.query_params["date_range"]
        except:
            return Response({"Error": "Date range must be provided"},\
                    status=status.HTTP_400_BAD_REQUEST)
        meal_plans = MealPlan.objects.filter(user=request.user.id, date_range = date_range)
        if not meal_plans:   
            return Response({"Error": "Meal plan with the date_range could not be found for the user"},\
                    status=status.HTTP_404_NOT_FOUND)
        serializer = MealPlanSerializer(meal_plans, many=True)
        return Response(serializer.data)


class MealPlanUpdateDeleteAPIView(APIView):
    def patch(self, request, pk):
        meal_plan = None
        try:
            meal_plan = MealPlan.objects.get(pk=pk, user=request.user.id)
        except MealPlan.DoesNotExist:
            return Response({"Error": "Meal plan with the ID could not be found for the user"},\
                 status=status.HTTP_404_NOT_FOUND)
        request.data['user'] = request.user.id
        serializer = MealPlanSerializer(meal_plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            meal_plan = MealPlan.objects.get(pk=pk, user=request.user.id)
        except MealPlan.DoesNotExist:
            return Response({"Error": "Meal plan with the ID could not be found for the user"},\
                 status=status.HTTP_404_NOT_FOUND)
        meal_plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

