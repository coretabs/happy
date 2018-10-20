from django.contrib.auth.models import User

from django_filters import rest_framework as filters
import django_filters
from django.db.models import Q


class UserFilter(filters.FilterSet):

    username_or_email = django_filters.CharFilter(method='username_email')

    class Meta:
        model = User
        fields = []
    
    def username_email(self, queryset, name, value):
        return queryset.filter(
           Q(username__icontains=value) | Q(email__icontains=value)
        )
