from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)