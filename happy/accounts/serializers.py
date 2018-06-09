from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """a serializer for our user profile objects"""

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'location', 'birth_date')


class UserSerializer(serializers.ModelSerializer):

    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='apiv1:post-detail')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'posts')
        extra_kwargs = {'password': {'write_only': True},
                        'posts': {'read_only': True}}
