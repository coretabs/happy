from rest_framework import serializers
from .models import Post, Like, Dislike
from fun.models import Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {}

        fields = ('id', 'author', 'content', 'created', 'modified',
                  'likes_count', 'dislikes_count', 'comments_count')
        model = Post

    def get_comments_count(self, post):
        """ get the number of comments for single post """

        return Comment.objects.filter(parent=post).count()

    def get_likes_count(self, post):
        """ get the number of likes for single post """

        return Like.objects.filter(post=post).count()

    def get_dislikes_count(self, post):
        """ get the number of dislikes for single post """

        return Dislike.objects.filter(post=post).count()


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created')


class DislikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dislike
        fields = ('id', 'user', 'post', 'created')
