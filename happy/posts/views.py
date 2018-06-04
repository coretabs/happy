# from django.shortcuts import render
from fun.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from .models import Post, Like, Dislike
from .serializers import PostSerializer, LikeSerializer, DislikeSerializer
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
    def likes(self, request, pk=None):
        likes = Like.objects.filter(post_id=pk)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def dislikes(self, request, pk=None):
        dislikes = Dislike.objects.filter(post_id=pk)
        serializer = DislikeSerializer(dislikes, many=True)
        return Response(serializer.data)


"""
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class DislikeViewSet(viewsets.ModelViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
"""
