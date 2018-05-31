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

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {'password':{'write_only': True},}


        #def create(self, validated_data):
#
 #           user_data = validated_data.pop('user')
  #          user = UserSerializer.create(UserSerializer(), validated_data=user_data)
   #         user, created = User.objects.update_or_create(user=user,
    #                                                                subject_major=validated_data.pop('subject_major'))

     #       return user