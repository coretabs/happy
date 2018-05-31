from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register('profiles', views.ProfileViewSet)
router.register('users', views.UserViewSet)
"""
urls:
api/v1/posts/
api/v1/posts/<id>
api/v1/posts/<id>/comments
api/v1/comments/
api/v1/comments/<id>

"""