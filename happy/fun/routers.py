from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

"""
urls:
api/v1/posts/
api/v1/posts/<id>
api/v1/posts/<id>/comments
api/v1/comments/
api/v1/comments/<id>

"""