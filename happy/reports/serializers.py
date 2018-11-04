from rest_framework import serializers
from django.core.exceptions import ValidationError
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string

from django.db.models import Count
from django.contrib.auth.models import User
from .models import PostReport


class PostReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model= PostReport
        extra_kwargs = {'reporter': {'read_only': True},
                        'post': {'read_only': True}}
        fields = ('reporter', 'post_id', 'reason', 'created',)
