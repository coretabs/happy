from rest_framework import routers
from .views import UserViewSet, ProfileViewSet  # , CommentViewSet
from posts.views import PostViewSet  # ,LikeViewSet, DislikeViewSet
# from posts.routers import postrouter

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

# router.register(r'likes', LikeViewSet)
# router.register(r'dislikes', DislikeViewSet)
# router.register(r'comments', CommentViewSet)

router.register('profiles', ProfileViewSet)
router.register('users', UserViewSet)

"""
urls:
api/v1/posts/
api/v1/posts/<id>
api/v1/posts/<id>/comments
api/v1/comments/
api/v1/comments/<id>
"""
