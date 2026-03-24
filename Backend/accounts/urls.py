from .views import UserDetailView, UserListCreateView
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/token', TokenObtainPairView.as_view(), name='token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),



  
    path('account/users', UserListCreateView.as_view()),
    path('account/users/<int:pk>', UserDetailView.as_view()),



]

