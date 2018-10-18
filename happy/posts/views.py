# from django.shortcuts import render
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
#from django.utils import timezone
#from datetime import timedelta
#from django.db.models import Case , When 
from django.db.models import Count
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action

from .models import Post
from .pagination import PostsLimitOffsetPagination, PostsPageNumberPagination
from .serializers import PostSerializer, SinglePostSerializer, PostLikesSerializer

from comments.models import Comment, Reply
from comments.serializers import CommentSerializer, ReplySerializer


class PostViewSet2(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class =  PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    pagination_class = PostsPageNumberPagination

    def get_queryset(self):
        #now = timezone.now()
        #date_day = timezone.now() - timedelta(hours=24) 
        data = Post.objects.order_by("?")
        return data

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
    
    def create(self, request):
        serializer = PostSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        post =  Post.objects.get(pk=pk)
        serializer = SinglePostSerializer(post,context={"request":request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        post =  Post.objects.get(pk=pk)
        serializer = PostSerializer(data=request.data, instance=post)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            post =  Post.objects.get(pk=pk)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def like(self, request , pk=None):
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
            post = Post.objects.get(pk=pk)
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                return Response("Like has been removed")
            else: 
                if post.dislikes.filter(id=request.user.id).exists():
                    post.dislikes.remove(request.user)
                post.likes.add(request.user)
                return Response("Like has been added")

    @action(detail=True, methods= ["get"])
    def dislike(self, request, pk=None):
            if not request.user.is_authenticated:
                return Response("Authentication credentials were not provided.")
            else:
                post = Post.objects.get(pk=pk)
                if post.dislikes.filter(id=request.user.id).exists():
                    post.dislikes.remove(request.user)
                    return Response("Dislike has been removed")
                else: 
                    if post.likes.filter(id=request.user.id).exists():
                        post.likes.remove(request.user)
                    post.dislikes.add(request.user)
                    return Response("Dislike has been added")

    @action(detail=True, methods=['get'])
    def likes(self, request , pk=None):
        likes = Post.objects.get(pk=pk).likes.all()
        serializer = PostLikesSerializer(likes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dislikes(self, request , pk=None):
        dislikes = Post.objects.get(pk=pk).dislikes.all()
        serializer = PostLikesSerializer(dislikes, many=True)
        return Response(serializer.data)