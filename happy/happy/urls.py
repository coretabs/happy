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
from fun.views import UserViewSet, UserProfileView, UserView
from posts.views import PostViewSet
# from fun.routers import router

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    #django admin
    path('admin/', admin.site.urls),
    
    #rest api
    path('api-auth/', include('rest_framework.urls')),
    path(r'api/v1/', include((router.urls,'apiv1'), namespace='apiv1')),
    path(r'api/v1/user/', UserView.as_view()),
    path(r'api/v1/user/profile/', UserProfileView.as_view()),
    
    #user management
    path('', include('accounts.urls')),
    path('accounts/', include('accounts.urls')), 
]
