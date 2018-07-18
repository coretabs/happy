# from django.shortcuts import render
from fun.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from .models import Post
from .serializers import PostSerializer
from comments.models import Comment, Reply
from comments.serializers import CommentSerializer, ReplySerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        reviews = Comment.objects.filter(parent_id=pk)
        serializer = CommentSerializer(reviews, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def like(self, request , pk=None):
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
        post = Post.objects.get(pk=pk)
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
            return Response("Dislike has been removed")
        else: 
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            post.dislikes.add(request.user)
            return Response("Dislike has been added")


class PostViewSet2(viewsets.ViewSet):
    serializer_class =  PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def list(self, request,):
        queryset = Post.objects.filter()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        # queryset =  Post.objects.filter()
        # post =  get_object_or_404(queryset, pk=pk)
        post =  Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
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
        post = Post.objects.get(pk=pk)
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
            return Response("Dislike has been removed")
        else: 
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            post.dislikes.add(request.user)
            return Response("Dislike has been added")