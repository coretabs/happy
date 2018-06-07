from rest_framework import serializers
from accounts.models import CustomUser, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """a serializer for our user profile objects"""

    # user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'location', 'birth_date')


class UserSerializer(serializers.ModelSerializer):

    # posts = serializers.PrimaryKeyRelatedField(
    #                                            many=True,
    #                                            queryset=models.Post.objects.all())
    # profile = ProfileSerializer(read_only=True)
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='apiv1:post-detail')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'posts')
        extra_kwargs = {'password': {'write_only': True},
                        'posts': {'read_only': True}}


# class UserSerializer(serializers.ModelSerializer):
#     posts=serializers.PrimaryKeyRelatedField(many=True,queryset=models.Post.objects.all())
#
#    class Meta:
#        fields = ('id','username','posts')
#        model = User
