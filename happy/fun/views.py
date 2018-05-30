from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions


from fun.permissions import IsOwnerOrReadOnly
from .models import Post, Comment, User
from .serializers import PostSerializer, CommentSerializer, UserSerializer

"""class PostList(generics.ListCreateAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
 """
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
           
    @detail_route(methods=['get'])
    def comments(self, request, pk=None):
        reviews = Comment.objects.filter(parent_id=pk)
        serializer = CommentSerializer(reviews, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def get_user(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        user=self.get_user(pk)
        serializer=UserSerializer(user)
        return Response(serializer.data)
