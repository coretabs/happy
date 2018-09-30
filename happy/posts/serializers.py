from rest_framework import serializers
from django.core.exceptions import ValidationError
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
from posts.pagination import CommentsPageNumberPagination, PostsPageNumberPagination

from django.db.models import Count
from .models import Post
from comments.models import Comment
from comments.serializers import TopCommentSerializer, CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField(source='FORMAT')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    top_comment = serializers.SerializerMethodField()
    
    class Meta:
        extra_kwargs = {'likes': {'read_only': True},
                        'dislikes': {'read_only': True}
        }
        model = Post
        fields = ("id","author","author_avatar","time_since",
                  "content","likes","dislikes","likes_count","dislikes_count",
                  "mediafile","comments_count","top_comment")

    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url

    def validate(self,data):
        null = None
        if len(data['content']) <=0  and data['mediafile'] is null :
            raise serializers.ValidationError(u'at least one field is required')
        return data


    def get_comments_count(self, post):
        """ get the number of comments for single post """

        return Comment.objects.filter(parent=post).count()

    def get_top_comment(self,post):
        data = Comment.objects.filter(parent=post).annotate(
            like_count=Count('likes')).order_by('-like_count').first()
        serializer = TopCommentSerializer(data).data
        if data == None:
            return None
        else:
            return serializer
   
    def get_likes_count(self,post):
        return post.likes_count()

    def get_dislikes_count(self, post):
        return post.dislikes_count()


"""    def to_representation(self, instance):
        ret = super(PostSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1], ret.items())))
        return ret
"""

class SinglePostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField(source='FORMAT')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    dislikes_count = serializers.ReadOnlyField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        extra_kwargs = {'likes': {'read_only': True},
                        'dislikes': {'read_only': True}
        }
        model = Post
        fields = ("id","author", "author_avatar","time_since",
                  "content","likes","dislikes","likes_count","dislikes_count",
                  "mediafile","comments_count","comments")

    def validate(self,data):
        null = None
        if len(data['content']) <=0  and data['mediafile'] is null :
            raise serializers.ValidationError(u'at least one field is required')
        return data

    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url
    
    def get_comments_count(self, post):
        """ get the number of comments for single post """
        return Comment.objects.filter(parent=post).count()

    def get_comments(self, post):
        
        data = Comment.objects.filter(parent=post)
        paginator = CommentsPageNumberPagination()
        page = paginator.paginate_queryset(data, self.context['request'])
        serializer = CommentSerializer(page, many=True).data
        return paginator.get_paginated_response(serializer).data



