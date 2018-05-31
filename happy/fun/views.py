from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class =  serializers.UserSerializer
    queryset = User.objects.all()
