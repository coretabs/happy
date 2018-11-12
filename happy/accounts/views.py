import os, requests
from rest_framework import viewsets, generics
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from fun.permissions import IsOwnerOrReadOnlyUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404

from posts.serializers import PostSerializer
from posts.models import Post
from posts.pagination import PostsLimitOffsetPagination, PostsPageNumberPagination
from rest_framework import serializers


# from rest_framework import permissions
from allauth.account.views import PasswordResetFromKeyView as PRV
from allauth.account.utils import perform_login
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from rest_auth.views import LogoutView as LV
from rest_auth.registration.views import VerifyEmailView as VEV
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token


from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout as django_logout
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from .models import Profile, Link
from .filters import UserFilter
from django.contrib.auth.models import User

from .serializers import (UserSerializer,
                        UserSocialLinksSerializer,
                        ProfileSerializer,
                        ResendConfirmSerializer, 
                        UserDetailsSerializer,
                         TokenSerializer)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(id=user.id)
        return profile

class UserSocialLinksViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = UserSocialLinksSerializer
    permission_classes = (IsAuthenticated,
                         IsOwnerOrReadOnlyUser, )
    
    def get_queryset(self):
        user = self.request.user
        return Link.objects.filter(user_id=user.profile.id)

    def create(self, request):
        links_count = Link.objects.filter(user_id= self.request.user.profile.id).count()
        links_to_create = []
        for link in request.data:
            if not 'id' in link:
                if not Link.objects.filter(social_app=link["social_app"],
                                    user_id= self.request.user.profile.id).exists():
                    if links_count < 4 and (links_count + len(links_to_create) < 4):
                        links_to_create.append(link)
            else:
                self.queryset.filter(id=link['id']).update(social_app=link['social_app'], 
                                                           social_link=link['social_link'])
        serializer = UserSocialLinksSerializer(data=links_to_create, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(author_id=user.id)
        return posts


class UserDetailsView(RetrieveUpdateAPIView):

    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


user_details_view = UserDetailsView.as_view()

class LogoutView(LV):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
            
        django_logout(request)

        return Response({"detail": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)

logout_view = LogoutView.as_view()

class ResendConfirmView(GenericAPIView):

    serializer_class = ResendConfirmSerializer

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Confirmation e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


resend_confirmation_view = ResendConfirmView.as_view()


class VerifyEmailView(VEV):
    token_model = TokenModel

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = self.serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        self.login_on_confirm(confirmation)
        return self.get_response()

    def login_on_confirm(self, confirmation):
        self.user = confirmation.email_address.user
        if self.user and self.request.user.is_anonymous:
            return perform_login(self.request,
                                 self.user,
                                 'none')

    def get_response(self):
        token = create_token(self.token_model, self.user, self.serializer)
        serializer_class = TokenSerializer

        serializer = serializer_class(instance=token,
                                          context={'request': self.request})

        return Response(serializer.data, status=status.HTTP_200_OK)


verify_email = VerifyEmailView.as_view()

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GetUserProfile(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    pagination_class = PostsPageNumberPagination

    def retrieve(self, request, username=None):
        queryset =  User.objects.all()
        user =  get_object_or_404(queryset, username=username)        
        serializer = UserDetailsSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods= ["get"])
    def posts(self, request, username=None):
        queryset = self.filter_queryset(self.get_queryset())
        user =  get_object_or_404(queryset, username=username)        
        posts = Post.objects.filter(author_id=user.id)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True, context={"request":request})
        return Response(serializer.data)


class UsersListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    pagination_class = PostsPageNumberPagination
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
    