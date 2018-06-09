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
