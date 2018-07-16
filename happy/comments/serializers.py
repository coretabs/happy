from .models import Comment, Reply, BaseComment
from posts.models import Post
from rest_framework import serializers


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
        
class CommentSerializer(BaseCommentSerializer):
    replies_count = serializers.SerializerMethodField()
    # replies = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}

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

