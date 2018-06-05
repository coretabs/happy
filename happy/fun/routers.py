from rest_framework import routers
from .views import UserViewSet, ProfileViewSet  # , CommentViewSet
from posts.views import PostViewSet  # ,LikeViewSet, DislikeViewSet
from comments.views import CommentViewSet, ReplyViewSet
# from posts.routers import postrouter

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register('profiles', ProfileViewSet)
router.register('users', UserViewSet)
# router.register(r'likes', LikeViewSet)
# router.register(r'dislikes', DislikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'replies', ReplyViewSet)

router.register('profiles', ProfileViewSet)
router.register('users', UserViewSet)

"""
urls:
api/v1/users/
api/v1/users/<id>/
api/v1/users/<id>/posts/
api/v1/users/<id>/profile/

api/v1/posts/
api/v1/posts/<id>/
api/v1/posts/<id>/comments

api/v1/profiles/
api/v1/profiles/<id>

api/v1/comments/
api/v1/comments/<id>/
api/v1/comments/<id>/replies

api/v1/replies/
api/v1/replies/<id>

"""
