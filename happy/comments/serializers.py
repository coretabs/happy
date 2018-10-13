from .models import Comment, Reply, BaseComment
from posts.models import Post
from rest_framework import serializers
from collections import OrderedDict
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.module_loading import import_string
from posts.pagination import CommentsPageNumberPagination, PostsPageNumberPagination
from django.db.models import Count


class BaseCommentSerializer(serializers.ModelSerializer):
   # likes_count = serializers.SerializerMethodField()
   # dislikes_count = serializers.SerializerMethodField()
    
    class Meta:
        fields = '__all__'
        model = BaseComment
   
class TopReplySerializer(BaseCommentSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField(source='FORMAT')
    likes_count = serializers.ReadOnlyField()
    dislikes_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Reply
        fields = ('id','author', "author_avatar",'content', "time_since",
                  'likes_count', 'dislikes_count')
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url


class CommentSerializer(BaseCommentSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField(source='FORMAT')
    likes_count = serializers.ReadOnlyField()
    dislikes_count = serializers.ReadOnlyField()
    replies_count = serializers.SerializerMethodField()
    top_reply = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()
    

    class Meta:
        model = Comment
        fields = ('id','author', "author_avatar","time_since", 'reaction','parent','content',
                  'likes_count','dislikes_count','replies_count', 'top_reply')

        extra_kwargs = {'parent': {'read_only': True},
                        'reaction': {'read_only': True}}
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url
    
    def get_replies_count(self, comment):
        """ get the number of replies for single comment """
        return Reply.objects.filter(parent=comment).count()
    
    def get_top_reply(self,comment):
        data = Reply.objects.filter(parent=comment).annotate(
            like_count=Count('likes')).order_by('-like_count').first()
        serializer = TopReplySerializer(data).data
        if data == None:
            return None
        else:
            return serializer
    
    def get_reaction(self, comment):
        reaction = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if comment.likes.filter(id=request.user.id).exists():
                reaction = 'liked'
            elif comment.dislikes.filter(id=request.user.id).exists():
                reaction = 'disliked'
            return reaction


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
    reaction = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        extra_kwargs = {'parent': {'read_only': True}}
        
        fields = ('id','author', "author_avatar",'content','parent',
                  "reaction",'likes_count','dislikes_count',"time_since")
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url
    
    def get_reaction(self, reply):
        reaction = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if reply.likes.filter(id=request.user.id).exists():
                reaction = 'liked'
            elif reply.dislikes.filter(id=request.user.id).exists():
                reaction = 'disliked'
            return reaction


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