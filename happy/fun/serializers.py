from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

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

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = comments = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                   view_name='apiv1:comment-detail')
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
            'comments',
        )
        model=models.Post

class UserSerializer(serializers.ModelSerializer):
    posts=serializers.PrimaryKeyRelatedField(many=True,queryset=models.Post.objects.all())

    class Meta:
        fields=('id','username','posts')
        model=User
