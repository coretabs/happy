from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet2
from comments.views import CommentViewSet2, ReplyViewSet2


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

"""
Test Routing Version 2
http://127.0.0.1:8000/api/v1/nested/posts/
http://127.0.0.1:8000/api/v1/nested/posts/<id>/
http://127.0.0.1:8000/api/v1/nested/posts/<id>/comments/
http://127.0.0.1:8000/api/v1/nested/posts/<id>/comments/<id>/
http://127.0.0.1:8000/api/v1/nested/posts/<id>/comments/<id>/replies/
http://127.0.0.1:8000/api/v1/nested/posts/<id>/comments/<id>/replies/<id>
"""