from django_filters import rest_framework as filters
import django_filters
from django.db.models import Q

from .models import Post


class PostFilter(filters.FilterSet):
    content = filters.CharFilter(field_name="content", lookup_expr='icontains')
    created_after = filters.DateFilter(field_name="created", lookup_expr='gt')
    created_before = filters.DateFilter(field_name="created", lookup_expr='lt')

    class Meta:
        model = Post
        fields = ['content', 'created_after', 'created_before']

