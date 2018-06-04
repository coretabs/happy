from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions

from .models import Profile
from .serializers import PostSerializer, CommentSerializer, UserSerializer, ProfileSerializer
from accounts.models import CustomUser as User
#from django.contrib.auth.models import User



class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


from fun.permissions import IsOwnerOrReadOnly
from .models import Post, Comment


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

