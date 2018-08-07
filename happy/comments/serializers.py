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
    replies = serializers.SerializerMethodField()
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

    def get_replies(self, instance):
        data = Reply.objects.filter(parent=instance)
        return data.values()

class ReplySerializer(BaseCommentSerializer):
    base_comment = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    

    class Meta:
        model = Reply
        extra_kwargs = {'likes': {'read_only': True},
                       'dislikes': {'read_only': True},
                       'parent': {'read_only': True}}
        
        fields =('base_comment','id','author','content','created',
                                'modified','parent','likes_count',
                                'dislikes_count','likes','dislikes')
    def get_base_comment(self,instance):
        data = Comment.objects.filter(pk = instance.parent_id)
        return data.values()

    def to_representation(self, instance):
        data = super(ReplySerializer, self).to_representation(instance)
        return {"Comment": data["base_comment"], "Replies":{"id":data['id'],'author':data["author"],'content':data["content"],
                                                            'created':data["created"],'modified':data["modified"],'parent':data["parent"],
                                                            'likes_count':data["likes_count"],'dislikes_count':data["dislikes_count"],
                                                            'likes':data["likes"],'dislikes':data["dislikes"]}}