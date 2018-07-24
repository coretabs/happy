import os, requests
from rest_framework import viewsets, generics
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from posts.serializers import PostSerializer
from posts.models import Post

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

from .models import Profile
from django.contrib.auth.models import User

from .serializers import (UserSerializer, 
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

class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(author_id=user.id)
        return posts


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        posts = Post.objects.filter(author_id=pk)
        context = {'request': request}
        serializer = PostSerializer(posts, context=context, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        profile = Profile.objects.filter(user_id=pk)
        context = {'request': request}
        serializer = ProfileSerializer(profile, context=context, many=True)
        return Response(serializer.data)


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

class UserDetailsView(RetrieveUpdateAPIView):

    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


user_details_view = UserDetailsView.as_view()

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
