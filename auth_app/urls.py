from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import user_otp, CustomUserViewSet

urlpatterns = [
    path('auth/users/<int:id>/otp/', user_otp, name="user-otp"),
    path('auth/users/<int:id>/delete/', CustomUserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),
    path('auth/users/<int:id>/set_password/', CustomUserViewSet.as_view({'post': 'set_password'}), name='user-set-password'),
    path('auth/users/<int:id>/set_username/', CustomUserViewSet.as_view({'post': 'set_username'}), name='user-set-username'),
]

urlpatterns = format_suffix_patterns(urlpatterns)