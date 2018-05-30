from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    posts=serializers.PrimaryKeyRelatedField(many=True,queryset=models.Post.objects.all())

    class Meta:
        fields=('id','username','posts')
        model=User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        extra_kwargs={
            #
        }
        fields=(
            'id',
            'content',
            'created',
            'modified',
            'author',
        )
        model=models.Post

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs={
            #
        }
        fields=(
            'id',
            'content',
            'author',
            'parent',
            'created',
            'modified',
        )
        model=models.Comment
