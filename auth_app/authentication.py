from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the token from the cookie
        token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if token is None:
            if "/auth/users/" in request.path or "/google/signup/" in request.path:
                return None
            raise AuthenticationFailed( "Access token missing in cookies.")

        # Validate the token
        validated_token = self.get_validated_token(token)
        if validated_token is None:
            raise AuthenticationFailed('Invalid token')

        # Get the user associated with this token
        user = self.get_user(validated_token)
        if user is None:
            raise AuthenticationFailed('No user matching this token was found')

        return (user, validated_token)
