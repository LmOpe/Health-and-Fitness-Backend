import time
import requests

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, action, permission_classes

from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.serializers import UsernameSerializer, PasswordSerializer

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken


from profiles.models import NotificationPreferences
from fudhouse.utils import hash_to_smaller_int, base64_encode
from fudhouse.settings import BASE_URL, FRONTEND_URL
from .models import User, OTP


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_auth(request):
    return Response({"Message": f"User is authenticated as {request.user.id}, {request.user.username}"})

class CustomUserViewSet(DjoserUserViewSet):
    def get_permissions(self):
        if self.action == 'set_password':
            return []
        return super().get_permissions()

    # Override the Djoser User delete method to allow deleting without passing current_pasword payload
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie(
                    settings.SIMPLE_JWT['AUTH_COOKIE'],
                    "No access",
                    max_age=0,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
        response.set_cookie(
                    settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    "No refresh",
                    max_age=0,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
        return response    

 # Override the Djoser User set password method to allow changing user's password without passing current_pasword payload
    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data,  context={'request': request}) # Use only the Password Serializer for validating new password payload
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=kwargs['id'])

        user.set_password(serializer.data["new_password"])
        user.save()

        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

 # Override the Djoser User set password method to allow changing user's username without passing current_pasword payload
    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        serializer = UsernameSerializer(data=request.data) # Use only the Username Serializer for validating new username payload
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(user, User.USERNAME_FIELD, new_username)
        user.save()
    
        return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_otp(request):    
    if request.method == 'GET':
        email = request.query_params.get("email")
        user = None

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
           return Response({"error": "User with mail address does not exist"}, status=status.HTTP_404_NOT_FOUND)

        otp = get_random_string(length=4, allowed_chars='0123456789')

        try:
            storedOTP = OTP.objects.get(user=user)
            storedOTP.delete()
        except OTP.DoesNotExist:
            pass

        newOTP = OTP(user=user, otp=otp, expiry_time=int(time.time()) + 300) # OTP expires in 5 minutes
        newOTP.save()

        send_mail(
            'Your OTP',
            f'Your OTP is: {otp}',
            'lawalmuhammed44@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent to user', 'user_id': user.id}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if 'otp' not in request.data:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)

        if 'user_id' not in request.data:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = request.data['user_id']
        storedOTP = None
        user=None

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
           return Response({"error": "User with given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            storedOTP = OTP.objects.get(user=user)
        except OTP.DoesNotExist:
            return Response({'error': 'No OTP can be found for user'}, status=status.HTTP_400_BAD_REQUEST)

        current_time = int(time.time())
        if current_time > storedOTP.expiry_time:
            # OTP has expired
            storedOTP.delete()
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        received_otp = request.data['otp']
        
        if received_otp == storedOTP.otp:
            storedOTP.delete()
            return Response({'message': 'OTP verified', 'user_id': user_id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect OTP'}, status=status.HTTP_400_BAD_REQUEST)


class ActivateUser(APIView):

    def get(self, request, uid, token):
        payload = {'uid': uid, 'token': token}
        url = f"{BASE_URL}/auth/users/activation/"
        response = requests.post(url, data = payload)

        if response.status_code == 204:
            frontend_url = f'{FRONTEND_URL}/account/activate/success'
            return HttpResponseRedirect(frontend_url) 
        if response.status_code == 400:
            return HttpResponseRedirect(f'{FRONTEND_URL}/account/activate')
        if response.status_code == 403:
            return HttpResponseRedirect(frontend_url)
        return HttpResponseRedirect(frontend_url)


class GoogleRedirectURIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Extract the authorization code from the request URL
        code = request.GET.get('code')
        return_response = HttpResponseRedirect(f"{settings.FRONTEND_URL}/diary")
        
        if code:
            # Prepare the request parameters to exchange the authorization code for an access token
            token_endpoint = 'https://oauth2.googleapis.com/token'
            token_params = {
                'code': code,
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'redirect_uri': f'{BASE_URL}/api/v1/auth/google/signup',  # Must match the callback URL configured in your Google API credentials
                'grant_type': 'authorization_code',
            }
            
            # Make a POST request to exchange the authorization code for an access token
            try:
                response = requests.post(token_endpoint, data=token_params)
            except:
                return HttpResponseRedirect(f"{settings.FRONTEND_URL}/log-in")
            
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                
                if access_token:
                    # Make a request to fetch the user's profile information
                    profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
                    headers = {'Authorization': f'Bearer {access_token}'}
                    profile_response = requests.get(profile_endpoint, headers=headers)
                    user = None
                    
                    if profile_response.status_code == 200:
                        data = {}
                        profile_data = profile_response.json()
                        # Proceed with user creation or login

                        uid = hash_to_smaller_int(profile_data['id'])
                      
                        try:
                            user = User.objects.get(id=uid)
                            
                            refresh = RefreshToken.for_user(user)
                            data['access'] = str(refresh.access_token)
                            data['refresh'] = str(refresh)
                            return_response.set_cookie(
                                settings.SIMPLE_JWT['AUTH_COOKIE'],
                                data['access'],
                                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            )
                            return_response.set_cookie(
                                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                                data['refresh'],
                                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            )
                            
                            return return_response

                        except User.DoesNotExist:
                            user = User.objects.create_user(id=uid,fullname=profile_data['name'], username=profile_data['name'],
                                                email=f"{profile_data['email']}-{uid}", password='NIL', is_active=True)
                            
                            notifpref = NotificationPreferences.objects.get_or_create(user=user)

                            refresh = RefreshToken.for_user(user)
                            data['access'] = str(refresh.access_token)
                            data['refresh'] = str(refresh)
                            return_response.set_cookie(
                                    settings.SIMPLE_JWT['AUTH_COOKIE'],
                                    data['access'],
                                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                                )
                            return_response.set_cookie(
                                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                                data['refresh'],
                                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            )
                        
                            return return_response
                        
        return Response({}, status.HTTP_400_BAD_REQUEST)


# class TwitterAuthRedirect(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         redirect_uri = f'{BASE_URL}/api/v1/auth/twitter/signup'  # Callback URL configured in Twitter Developer Dashboard
#         auth_url = f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id={settings.SOCIAL_AUTH_TWITTER_OAUTH2_KEY}&redirect_uri={redirect_uri}&scope=users.read%20tweet.read%20offline.access&state=state&code_challenge=challenge&code_challenge_method=plain"
#         #auth_url = f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id=RDFOTkJ2T3dZUFZHZTVtZUgycnc6MTpjaQ&redirect_uri=http://127.0.0.1:8000/api/v1/auth/twitter/signup&scope=users.read%20tweet.read%20offline.access&state=state&code_challenge=challenge&code_challenge_method=plain"
        
#         return redirect(auth_url)


class TwitterRedirectURIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')
        return_response = HttpResponseRedirect(f"{settings.FRONTEND_URL}/diary")


        if code:
            token_url = 'https://api.twitter.com/2/oauth2/token'
            token_params = {
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': f'{BASE_URL}/api/v1/auth/twitter/signup',
                'code_verifier': 'challenge'
            }

            # Client ID and Client Secret obtained from Twitter Developer account
            client_id = settings.SOCIAL_AUTH_TWITTER_OAUTH2_KEY
            client_secret = settings.SOCIAL_AUTH_TWITTER_OAUTH2_SECRET

            # Concatenate client ID and client secret with a colon
            credentials = f"{client_id}:{client_secret}"

            # Encode the concatenated string using Base64
            base64_credentials = base64_encode(credentials)

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {base64_credentials}'
            }

            response = requests.post(token_url, headers=headers, data=token_params)
          
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                if access_token:
                    user_info_url = 'https://api.twitter.com/2/users/me'
                    headers = {'Authorization': f'Bearer {access_token}'}
                    user_info_response = requests.get(user_info_url, headers=headers)

                    if user_info_response.status_code == 200:
                        data = {}
                        user_info = user_info_response.json()['data']
                        # Proceed with user creation or login
                        
                        uid = user_info['id']
                      
                        try:
                            user = User.objects.get(id=uid)
                            
                            refresh = RefreshToken.for_user(user)
                            data['access'] = str(refresh.access_token)
                            data['refresh'] = str(refresh)
                            return_response.set_cookie(
                                settings.SIMPLE_JWT['AUTH_COOKIE'],
                                data['access'],
                                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            )
                            return_response.set_cookie(
                                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                                data['refresh'],
                                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            )
                            
                            return return_response

                        except User.DoesNotExist:
                            user = User.objects.create_user(id=uid, fullname=user_info['name'], username=user_info['username'],
                                                            email=f"-{uid}", password='Nil', is_active=True)
                            
                            notifpref = NotificationPreferences.objects.get_or_create(user=user)

                            refresh = RefreshToken.for_user(user)
                            data['access'] = str(refresh.access_token)
                            data['refresh'] = str(refresh)
                            return_response.set_cookie(
                                    settings.SIMPLE_JWT['AUTH_COOKIE'],
                                    response.data['access'],
                                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                                )
                            return_response.set_cookie(
                                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                                response.data['refresh'],
                                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            )
                        
                            return return_response
        
        return Response({}, status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            response.data['access'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            response.data['refresh'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        del response.data['access']
        del response.data['refresh']
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Get refresh token from cookies
        refresh_token = request.COOKIES.get('refresh')

        if not refresh_token:
            return Response({"detail": "Refresh token missing in cookies."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        # Set the new access token in an HTTPOnly cookie
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE'],
            response.data['access'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )

        del response.data['access']
        
        return response

class CustomLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie(
                    settings.SIMPLE_JWT['AUTH_COOKIE'],
                    "No access",
                    max_age=0,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
        response.set_cookie(
                    settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    "No refresh",
                    max_age=0,
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
        return response