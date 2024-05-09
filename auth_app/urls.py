from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import user_otp, CustomUserViewSet, GoogleAuthRedirect, \
    GoogleRedirectURIView, TwitterAuthRedirect, \
    TwitterRedirectURIView,test_auth, ActivateUser

urlpatterns = [
    path('users/otp/', user_otp, name="user-otp"),
    path('users/<int:id>/delete/', CustomUserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),
    path('users/<int:id>/set_password/', CustomUserViewSet.as_view({'post': 'set_password'}), name='user-set-password'),
    path('users/set_username/', CustomUserViewSet.as_view({'post': 'set_username'}), name='user-set-username'),
    path('users/account/activate/<str:uid>/<str:token>', ActivateUser.as_view(), name="activate-user"),
    path("google-signup/", GoogleAuthRedirect.as_view(), name="google-redirect-user"),
    path("google/signup/", GoogleRedirectURIView.as_view(), name="google-handle-redirect"),   
    path("twitter-signup/", TwitterAuthRedirect.as_view(), name="twitter-redirect-user"),
    path("twitter/signup/", TwitterRedirectURIView.as_view(), name="twitter-handle-redirect"),   
    path("test-auth/", test_auth), 
]