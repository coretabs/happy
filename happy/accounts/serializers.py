import re
from .models import Profile, Link
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.defaultfilters import filesizeformat
from rest_framework import serializers
from rest_framework import serializers, exceptions
from rest_auth.registration.serializers import RegisterSerializer as RS
from rest_auth.serializers import LoginSerializer as LS
from rest_auth.models import TokenModel

from avatar.models import Avatar
from avatar.signals import avatar_updated
from allauth.account.forms import ResetPasswordForm, default_token_generator
from allauth.account.utils import send_email_confirmation, user_pk_to_url_str
from allauth.account.forms import UserTokenForm
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from allauth.account.models import EmailAddress

UserModel = get_user_model()

class ListUserSociaLinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Link
        fields = ('social_app','social_link')

    def to_representation(self, instance):
        data = super(ListUserSociaLinkSerializer, self).to_representation(instance)
        return {data["social_app"]: data["social_link"]}

class ProfileSerializer(serializers.ModelSerializer):
    """a serializer for our user profile objects"""
    link  = ListUserSociaLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = ( 'first_name','last_name','displayed_name','bio', 'location', 'birth_date','link')
        extra_kwargs = {
                    'first_name':{'write_only':True},
                    'last_name':{'write_only':True},
                    'displayed_name':{'read_only':True}}

    def validate(self, data):
        pattern = "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]+[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]+[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]*$"
        compiler = re.compile(pattern)
        if not compiler.match(data["first_name"]):
            raise serializers.ValidationError(
                _("Make sure it contains only letters."))
        if not compiler.match(data["last_name"]):
            raise serializers.ValidationError(
                _("Make sure it contains only letters."))
            
        return data

class DisplayUserName(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField(source='displayed_name')

    class Meta:
        model = Profile
        fields = ('display_name',)

class UserSocialLinksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Link
        fields = ('id','social_app','social_link')

class UserSerializer(serializers.ModelSerializer):

    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='apiv1:post-detail')
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'posts')
        extra_kwargs = {'password': {'write_only': True},
                        'posts': {'read_only': True}}

class RegisterSerializer(RS):
    name = serializers.CharField(
        max_length=100,
        min_length=5,
        required=True
    )

    def validate_name(self, name):
        pattern = "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]+ [a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]+[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي ]*$"
        compiler = re.compile(pattern)
        if not compiler.match(name):
            raise serializers.ValidationError(
                _("Make sure it contains only letters and spaces."))

        return name

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('name', '')
        }



class LoginSerializer(LS):

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = self._validate_username_email(username, email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        email_address = user.emailaddress_set.get(email=user.email)
        if not email_address.verified:
            raise exceptions.PermissionDenied('not verified')

        attrs['user'] = user
        return attrs

class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if not email_address_exists(email):
            raise serializers.ValidationError(_("The e-mail address is not assigned "
                                                "to any user account"))
        return email

    def save(self, *args, **kwargs):
        request = self.context.get('request')

        current_site = get_current_site(request)
        email = self.validated_data["email"]

        user = UserModel.objects.get(email__iexact=email)

        token_generator = kwargs.get("token_generator", default_token_generator)
        temp_key = token_generator.make_token(user)

        path = "/reset-password/{}/{}".format(user_pk_to_url_str(user), temp_key)
        url = request.build_absolute_uri(path)
        context = {"current_site": current_site,
                   "user": user,
                   "password_reset_url": url,
                   "request": request}

        get_adapter().send_mail(
            'account/email/password_reset_key',
            email,
            context)

        return email


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    key = serializers.CharField()

    def validate_new_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        self.user_token_form = UserTokenForm(data={'uidb36': attrs['uid'], 'key': attrs['key']})

        if not self.user_token_form.is_valid():
            raise serializers.ValidationError(_("Invalid Token"))

        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))

        self.password = attrs['new_password1']

        return attrs

    def save(self):
        user = self.user_token_form.reset_user
        get_adapter().set_password(user, self.password)
        return user

class ResendConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password_reset_form_class = ResetPasswordForm

    def validate(self, attrs):
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return attrs

    def save(self):
        request = self.context.get('request')
        User = get_user_model()
        email = self.reset_form.cleaned_data["email"]
        user = User.objects.get(email__iexact=email)
        send_email_confirmation(request, user, True)
        return email

from posts.serializers import PostSerializer
class UserDetailsSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    email_status = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    profile = ProfileSerializer()
    avatar = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'email_status', 'profile', 'avatar', 'avatar_url', 'posts')

    def get_email_status(self, obj):
        email_address = EmailAddress.objects.get(user=obj)
        return email_address.verified

    def get_avatar_url(self, obj, size=settings.AVATAR_DEFAULT_SIZE):
        for provider_path in settings.AVATAR_PROVIDERS:
            provider = import_string(provider_path)
            avatar_url = provider.get_avatar_url(obj, size)
            if avatar_url:
                return avatar_url

    def validate_name(self, name):
        pattern = "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]+[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]+[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ðء-ي]*$"
        compiler = re.compile(pattern)
        if not compiler.match(name):
            raise serializers.ValidationError(
                _("Make sure it contains only letters and spaces."))

        return name

    def validate_avatar(self, avatar):
        if settings.AVATAR_ALLOWED_FILE_EXTS:
            root, ext = os.path.splitext(avatar.name.lower())
            if ext not in settings.AVATAR_ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(settings.AVATAR_ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. "
                          "Authorized extensions are : %(valid_exts_list)s")
                raise serializers.ValidationError(error %
                                            {'ext': ext,
                                             'valid_exts_list': valid_exts})

        if avatar.size > settings.AVATAR_MAX_SIZE:
            error = _("Your file is too big: %(size)s, "
                      "the maximum allowed size is: %(max_valid_size)s")

            raise serializers.ValidationError(error % {
                'size': filesizeformat(avatar.size),
                'max_valid_size': filesizeformat(settings.AVATAR_MAX_SIZE)
            })


    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email, exclude_user=self.context.get('request').user):
            raise serializers.ValidationError(_("A user is already registered with this e-mail address."))
        return email

    def update(self, instance, validated_data):
        request = self.context.get('request')

        profile = validated_data.get('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        
        if profile :
            bio = profile.get("bio")
            location = profile.get("location")
            birth_date = profile.get("birth_date")
            first_name = profile.get("first_name")
            last_name = profile.get("last_name")
            if bio and bio != instance.profile.bio :
                instance.profile.bio = bio
            if location and location != instance.profile.location:
                instance.profile.location = location
            if birth_date and birth_date != instance.profile.birth_date:
                instance.profile.birth_date = birth_date 
            if first_name and first_name != instance.profile.first_name:
                instance.profile.first_name = first_name
            if last_name and last_name != instance.profile.last_name:
                instance.profile.last_name = last_name  

        email = validated_data.get('email', None)
        if email and email != instance.email:
            adapter = get_adapter()
            adapter.send_mail('account/email/email_change', instance.email, {})
            email_address = EmailAddress.objects.get(user=instance, verified=True)
            email_address.change(request, email, True)
            instance.email = email

        if 'avatar' in request.FILES:
            avatar = Avatar(user=instance, primary=True)
            image_file = request.FILES['avatar']
            avatar.avatar.save(image_file.name, image_file)
            avatar.save()
            avatar_updated.send(sender=Avatar, user=instance, avatar=avatar)

        instance.save()

        # sync_sso(instance)

        return instance

class TokenSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = TokenModel
        fields = ('key', 'user')