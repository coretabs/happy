from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]