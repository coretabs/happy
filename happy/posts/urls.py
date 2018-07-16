from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet2, CommentViewSet2, ReplyViewSet2


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet2, base_name='posts')

post_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
post_router.register(r'comments', CommentViewSet2, base_name='comments')

comment_router = routers.NestedSimpleRouter(post_router, r'comments', lookup='comment')
comment_router.register(r'replies', ReplyViewSet2, base_name='replies')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(post_router.urls)),
    path(r'', include(comment_router.urls)),
]