"""happy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin

from rest_framework import routers
from accounts.views import (UserViewSet, UserProfileView,
                            UserView, UserPostsView)
from posts.views import PostViewSet
from comments.views import CommentViewSet, ReplyViewSet

# from fun.routers import router

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(f'replies', ReplyViewSet)



urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),

    # rest api
    path('api-auth/', include('rest_framework.urls')),
    path(r'api/v1/', include((router.urls, 'apiv1'), namespace='apiv1')),
    path(r'api/v1/user/', UserView.as_view()),
    path(r'api/v1/user/profile/', UserProfileView.as_view()),
    path(r'api/v1/user/posts/', UserPostsView.as_view()),


    # user management
    # path('', include('accounts.urls')),
    # path('accounts/', include('accounts.urls')),
]
"""
urls:

api/v1/user/
api/v1/user/profile
api/v1/user/posts

api/v1/users/
api/v1/users/<id>/
api/v1/users/<id>/posts/
api/v1/users/<id>/profile/

api/v1/posts/
api/v1/posts/<id>/
api/v1/posts/<id>/comments
api/v1/posts/<id>/like
api/v1/posts/<id>/dislike

api/v1/comments/
api/v1/comments/<id>
api/v1/comments/<id>/replies
api/v1/comments/<id>/like
api/v1/comments/<id>/dislike

api/v1/replies/
api/v1/replies/<id>/
api/v1/replies/<id>/like
api/v1/replies/<id>/dislike
"""
