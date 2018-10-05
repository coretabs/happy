from .models import Comment, Reply, BaseComment
from posts.models import Post
from rest_framework import serializers
from collections import OrderedDict
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.module_loading import import_string
from posts.pagination import CommentsPageNumberPagination, PostsPageNumberPagination


class BaseCommentSerializer(serializers.ModelSerializer):
   # likes_count = serializers.SerializerMethodField()
   # dislikes_count = serializers.SerializerMethodField()
    
    class Meta:
        fields = '__all__'
        model = BaseComment
   
""" def get_likes_count(self, comment):
        return comment.likes_count()

    def get_dislikes_count(self, comment):
        return comment.dislikes_count()
"""
"""
    def to_representation(self, instance):
        ret = super(BaseCommentSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1], ret.items())))
        return ret
        """
class CommentSerializer(BaseCommentSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField(source='FORMAT')
    likes_count = serializers.ReadOnlyField()
    dislikes_count = serializers.ReadOnlyField()
    replies_count = serializers.SerializerMethodField()
    

    class Meta:
        model = Comment
        fields = ('id','author', "author_avatar","time_since",'parent','content',
                  'likes','dislikes','likes_count','dislikes_count','replies_count')

        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url
    
    def get_replies_count(self, comment):
        """ get the number of replies for single comment """
        return Reply.objects.filter(parent=comment).count()


class CommentSerializerInsidePostInstance(BaseCommentSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField(source='FORMAT')
    likes_count = serializers.ReadOnlyField()
    dislikes_count = serializers.ReadOnlyField()
    replies_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    

    class Meta:
        model = Comment
        fields = ('id','author', "author_avatar","time_since",'parent','content',
                  'likes','dislikes','likes_count','dislikes_count','replies_count',
                  'replies')

        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url
    
    def get_replies_count(self, comment):
        """ get the number of replies for single comment """
        return Reply.objects.filter(parent=comment).count()

    def get_replies(self, instance):
        data = Reply.objects.filter(parent=instance)
        paginator = CommentsPageNumberPagination()
        page = paginator.paginate_queryset(data, self.context['request'])
        serializer = ReplySerializer(page, many=True).data
        return paginator.get_paginated_response(serializer).data

        
class TopCommentSerializer(BaseCommentSerializer):
    # replies_count = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id','author', "author_avatar",'content')
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url
    
    """
    def get_replies_count(self, comment):
        """ """get the number of replies for single comment""" """
        return Reply.objects.filter(parent=comment).count()
    """
    
class ReplySerializer(BaseCommentSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField(source='FORMAT')
    likes_count = serializers.ReadOnlyField()
    dislikes_count = serializers.ReadOnlyField()

    class Meta:
        model = Reply
        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}
        
        fields = ('id','author', "author_avatar",'content','parent',
                  'likes','dislikes','likes_count','dislikes_count',"time_since")
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url


class CommentLikesSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("username","avatar")


    def get_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj, size)
            if avatar_url:
                return avatar_url