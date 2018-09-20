from .models import Comment, Reply, BaseComment
from posts.models import Post
from rest_framework import serializers
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string


class BaseCommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    
    class Meta:
        fields = '__all__'
        model = BaseComment
   
    def get_likes_count(self, comment):
        return comment.likes_count()

    def get_dislikes_count(self, comment):
        return comment.dislikes_count()

    def to_representation(self, instance):
        ret = super(BaseCommentSerializer, self).to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(list(filter(lambda x: x[1], ret.items())))
        return ret
        
class CommentSerializer(BaseCommentSerializer):
    replies_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id','created','modified','author', "author_avatar",'parent','content','likes','dislikes','likes_count',
                                'dislikes_count','replies_count','replies')

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
        return data.values()

class TopCommentSerializer(BaseCommentSerializer):
    replies_count = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id','author', "author_avatar",'content','likes','dislikes','parent','likes_count',
                                'dislikes_count','replies_count','created','modified')
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url
    
    def get_replies_count(self, comment):
        """ get the number of replies for single comment """
        return Reply.objects.filter(parent=comment).count()
    
class ReplySerializer(BaseCommentSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}
        
        fields = ('id','created','modified','author', "author_avatar",'content','likes','dislikes','likes_count',
                                'dislikes_count')
    
    def get_author_avatar(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj.author, size)
            if avatar_url:
                return avatar_url