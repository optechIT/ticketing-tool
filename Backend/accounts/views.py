from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response




from rest_framework import generics
from .models import CustomUser

from .serializers import (
    UserListSerializer,
    UserCreateSerializer,
    UserDetailSerializer
)



class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer


