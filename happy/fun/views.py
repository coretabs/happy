from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions


from fun.permissions import IsOwnerOrReadOnly
from . import models 
from . import serializers

class PostList(generics.ListCreateAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)

class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=serializers.UserSerializer

class UserDetail(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=serializers.UserSerializer

    def get_user(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        user=self.get_user(pk)
        serializer=serializers.UserSerializer(user)
        return Response(serializer.data)
