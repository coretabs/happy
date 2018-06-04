from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from posts.serializers import PostSerializer
from posts.models import Post
from rest_framework import permissions

from .models import Comment, User, Profile

from .serializers import CommentSerializer, UserSerializer, ProfileSerializer

from django.contrib.auth.models import User

# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        profile = Profile.objects.filter(user_id=pk)
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        posts = Post.objects.filter(author_id=pk)
        context = {'request': request}
        serializer = PostSerializer(posts, context=context, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
