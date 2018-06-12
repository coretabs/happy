# from django.shortcuts import render
from fun.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from .models import Post
from .serializers import PostSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer
# Create your views here.


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

"""
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class DislikeViewSet(viewsets.ModelViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
"""
