from rest_framework import serializers

from . import models

from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """a serializer for our user profile objects"""

    #user = UserSerializer(read_only=True)

    class Meta:
        model = models.Profile
        fields = ('user', 'bio', 'location', 'birth_date')


class UserSerializer(serializers.ModelSerializer):

    #posts = serializers.PrimaryKeyRelatedField(many=True,queryset=models.Post.objects.all())
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {'password':{'write_only': True},}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs={
            #
        }
        fields=(
            'id',
            'content',
            'author',
            'parent',
            'created',
            'modified',
        )
        model=models.Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='apiv1:comment-detail')
    class Meta:
        extra_kwargs={
            #
        }
        fields=(
            'id',
            'content',
            'created',
            'modified',
            'author',
            'comments',
        )
        model=models.Post

#class UserSerializer(serializers.ModelSerializer):
 #   posts=serializers.PrimaryKeyRelatedField(many=True,queryset=models.Post.objects.all())
#
 #   class Meta:
  #      fields=('id','username','posts')
   #     model=User
