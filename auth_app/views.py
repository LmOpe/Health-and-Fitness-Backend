import time
from datetime import timedelta

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404,render
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action, permission_classes

from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.serializers import UsernameSerializer, PasswordSerializer

from .models import User

class CustomUserViewSet(DjoserUserViewSet):
    # Override the Djoser User delete method to allow deleting without passing current_pasword payload
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

 # Override the Djoser User set password method to allow changing user's password without passing current_pasword payload
    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data) # Use only the Password Serializer for validating new password payload
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

 # Override the Djoser User set password method to allow changing user's username without passing current_pasword payload
    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        serializer = UsernameSerializer(data=request.data) # Use only the Username Serializer for validating new username payload
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(user, User.USERNAME_FIELD, new_username)
        user.save()
    
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_otp(request, id):    
    if request.method == 'GET':
        email = request.query_params.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if 'otp' in request.session:
            del request.session['otp']

        otp = get_random_string(length=4, allowed_chars='0123456789')
        
        request.session['otp'] = {
            'otp': otp,
            'expiry_time': int(time.time()) + 60  # OTP expires after 60 seconds
        }

        send_mail(
            'Your OTP',
            f'Your OTP is: {otp}',
            'lawalmuhammed44@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent to user'}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if 'otp' not in request.data:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'otp' not in request.session:
            return Response({'error': 'OTP session expired'}, status=status.HTTP_400_BAD_REQUEST)

        otp_data = request.session['otp']

        current_time = int(time.time())
        if current_time > otp_data['expiry_time']:
            # OTP has expired
            del request.session['otp']
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        received_otp = request.data['otp']
        
        stored_otp = otp_data['otp']
        
        if received_otp == stored_otp:
            del request.session['otp']
            return Response({'message': 'OTP verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect OTP'}, status=status.HTTP_400_BAD_REQUEST)