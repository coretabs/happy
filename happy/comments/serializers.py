from .models import Comment, Reply, BaseComment
from posts.models import Post
from rest_framework import serializers
from collections import OrderedDict



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

    class Meta:
        model = Comment
        fields = ('id','created','modified','author','parent','content','likes','dislikes','likes_count',
                                'dislikes_count','replies_count','replies')

        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}

    def get_replies_count(self, comment):
        """ get the number of replies for single comment """
        return Reply.objects.filter(parent=comment).count()

    def get_replies(self, instance):
        data = Reply.objects.filter(parent=instance)
        return data.values()

class TopCommentSerializer(BaseCommentSerializer):
    replies_count = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ('id','author','content','likes','dislikes','parent','likes_count',
                                'dislikes_count','replies_count','created','modified')

    def get_replies_count(self, comment):
        """ get the number of replies for single comment """
        return Reply.objects.filter(parent=comment).count()
    
class ReplySerializer(BaseCommentSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Reply
        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}
        
        fields = '__all__'