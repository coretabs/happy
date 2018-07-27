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
from django.views.generic import TemplateView

from rest_framework import routers
from accounts.views import UserViewSet, UserSocialLinksViewSet
from posts.views import PostViewSet
from comments.views import CommentViewSet, ReplyViewSet


# from fun.routers import router

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('social', UserSocialLinksViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(f'replies', ReplyViewSet)



urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # rest api
    path('api-auth/', include('rest_framework.urls')),
    path(r'api/v1/', include((router.urls, 'apiv1'), namespace='apiv1')),
    path(r'api/v1/auth/', include('accounts.urls'), name='auth-api'),

    # user management
    path(r'accounts/', include('allauth.urls')),
    path(r'avatar/', include('avatar.urls')),
    
    path(r'api/v1/nested/', include('posts.urls')),

]




from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





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
