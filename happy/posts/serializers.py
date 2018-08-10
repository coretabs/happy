from rest_framework import serializers
from django.core.exceptions import ValidationError
from collections import OrderedDict

from django.db.models import Count
from .models import Post
from comments.models import Comment
from comments.serializers import TopCommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
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
        fields = ("id","author","time_since","created","modified","content","likes",
                                 "dislikes","likes_count","dislikes_count",
                                 "mediafile","comments_count","top_comment")

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
        return TopCommentSerializer(data).data
   
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


