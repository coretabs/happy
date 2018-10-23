from django.urls import path, include
from .views import PostReportViewSet

urlpatterns = [
    # django admin
    path('', PostReportViewSet.as_view({'get': 'list'}))
]