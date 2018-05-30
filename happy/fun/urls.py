from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns=[
    #path('',views.ListCreatePosts.as_view(), name='all_posts'),
    path('v1/posts/',views.PostList.as_view()),
    path('v1/posts/<int:pk>/',views.PostDetail.as_view()),   
    #path('v1/posts/<int:pk>/comments',views.CommentDetial.as_view()),
    path('v1/users/', views.UserList.as_view()),
    path('v1/users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)