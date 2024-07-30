from django.urls import path

from .views import user_otp, CustomUserViewSet, \
    GoogleRedirectURIView, TwitterRedirectURIView,test_auth, ActivateUser,\
    CustomTokenRefreshView, CustomLogoutView, CustomTokenObtainPairView

urlpatterns = [
    path('users/otp/', user_otp, name="user-otp"),
    path('users/<int:id>/delete/', CustomUserViewSet.as_view({'delete': 'destroy'}), \
         name='user-delete'),
    path('users/<int:id>/set_password/', CustomUserViewSet.as_view({'post': 'set_password'}),\
          name='user-set-password'),
    path('users/set_username/', CustomUserViewSet.as_view({'post': 'set_username'}), name='user-set-username'),
    path('users/account/activate/<str:uid>/<str:token>', ActivateUser.as_view(), name="activate-user"),
    #path("google-signup/", GoogleAuthRedirect.as_view(), name="google-redirect-user"),
    path("google/signup/", GoogleRedirectURIView.as_view(), name="google-handle-redirect"),
   # path("twitter-signup/", TwitterAuthRedirect.as_view(), name="twitter-redirect-user"),
    path("twitter/signup/", TwitterRedirectURIView.as_view(), name="twitter-handle-redirect"),  
    path("test-auth/", test_auth),
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/logout/', CustomLogoutView.as_view(), name='jwt-logout'),

]