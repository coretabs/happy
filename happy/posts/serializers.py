from rest_framework import serializers
from .models import Post
from comments.models import Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {}

        model = Post
        fields = '__all__'

    def validate(self,data):
        null = None
        if len(data['content']) <=0  and data['mediafile'] is null :
            raise serializers.ValidationError(u'at least one field is required')
        return data


    def get_comments_count(self, post):
        """ get the number of comments for single post """

        return Comment.objects.filter(parent=post).count()

    def get_likes_count(self,post):
        return post.likes_count()

    def get_dislikes_count(self, post):
        return post.dislikes_count()



