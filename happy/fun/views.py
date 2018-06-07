from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from posts.serializers import PostSerializer
from posts.models import Post
from rest_framework import permissions

from accounts.models import CustomUser, Profile

from .serializers import UserSerializer, ProfileSerializer



class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    def get_object(self):
        profile = Profile.objects.get(id=self.request.user.id)
        return profile

class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

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
