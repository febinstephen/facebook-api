# coding=utf-8

import datetime

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password

from rest_framework import serializers

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):

    """
    Serializer for user login.
    Validates an email-password pair and authenticate it for login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
        else:
            raise serializers.ValidationError(_('Invalid credentials.'))

        attrs['user'] = user
        return attrs


class UserEmailRegisterSerializer(serializers.Serializer):

    """
    Serializer for user registration.
    Creates a user instance.
    """

    fname = serializers.CharField()
    lname = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField()
    password = serializers.CharField(required=False, allow_blank=True)
    provider = serializers.CharField(required=False, allow_blank=True)
    access_token = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ('fname','lname','phone','email','password','provider','access_token')

    def __init__(self, *args, **kwargs):
        super(UserEmailRegisterSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):

        has_provider = data.get('provider')
        password = data.get('password')
        email = data.get('email')
        if not has_provider:
            if not password or password == '':
                raise serializers.ValidationError(_('Password should not be empty.'))

        try:
            User.objects.get(email=email)
            raise serializers.ValidationError(_('User with this email already exists.'))
        except User.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        validated_data.update({
            'username':validated_data['email']
        })
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['fname'],
                                   last_name=validated_data['lname'],
                                   email=validated_data['email'],
                                   mobile=validated_data.get('phone',None))
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserEmailRegisterV2Serializer(serializers.Serializer):

    """
    Serializer for user registration.
    Creates a user instance.
    """

    fname = serializers.CharField()
    lname = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField()
    password = serializers.CharField(required=False, allow_blank=True)
    dob = serializers.CharField(required=False, allow_blank=True)
    provider = serializers.CharField(required=False, allow_blank=True)
    access_token = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ('fname','lname','phone','email','password','provider','access_token', 'gender', 'dob')

    def __init__(self, *args, **kwargs):
        super(UserEmailRegisterV2Serializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        has_provider = data.get('provider')
        password = data.get('password')
        email = data.get('email')
        if not has_provider:
            if not password or password == '':
                raise serializers.ValidationError(_('Password should not be empty.'))

        try:
            User.objects.get(email=email)
            raise serializers.ValidationError(_('User with this email already exists.'))
        except User.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        dob = validated_data.get('dob', None)
        validated_data.update({
            'username':validated_data['email']
        })
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['fname'],
                                   last_name=validated_data['lname'],
                                   email=validated_data['email'],
                                   gender=validated_data.get('gender',None),
                                   mobile=validated_data.get('phone',None))

        if dob:
            user_dob = datetime.datetime.strptime(dob, "%d/%m/%Y").date()
            user.dob = user_dob
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving user profile details.
    """

    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    oauth = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'fname', 'lname','email','role', 'phone', 'address','oauth')

    def get_fname(self, obj):
        return '%s'%(obj.first_name)

    def get_lname(self, obj):
        return '%s'%(obj.last_name)

    def get_phone(self, obj):
        return '%s'%(obj.mobile) if obj.mobile else ''

    def get_address(self, obj):
        return ""

    def get_oauth(self, obj):
        as_fb_user = SocialAccount.objects.filter(user_id= obj.id, provider='facebook')
        as_gp_user = SocialAccount.objects.filter(user_id= obj.id, provider='google')
        return {
            'facebook':as_fb_user.count() > 0,
            'google':as_gp_user.count() > 0
        }


class UserProfileV2Serializer(serializers.ModelSerializer):

    """
    Serializer for retrieving user profile details.
    """

    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    gender = serializers.CharField()
    oauth = serializers.SerializerMethodField()
    checkins = serializers.SerializerMethodField()
    points = serializers.CharField()
    image_url = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'fname', 'lname','email','role', 'phone', 'address','oauth', 'gender', 'checkins', 'points', 'image_url', 'dob')

    def get_fname(self, obj):
        return '%s'%(obj.first_name)

    def get_lname(self, obj):
        return '%s'%(obj.last_name)

    def get_phone(self, obj):
        return '%s'%(obj.mobile) if obj.mobile else ''

    def get_address(self, obj):
        return ""

    def get_dob(self, obj):
        return obj.dob.strftime('%d/%m/%Y') if obj.dob else ""

    def get_oauth(self, obj):
        as_fb_user = SocialAccount.objects.filter(user_id= obj.id, provider='facebook')
        as_gp_user = SocialAccount.objects.filter(user_id= obj.id, provider='google')
        return {
            'facebook':as_fb_user.count() > 0,
            'google':as_gp_user.count() > 0
        }

    def get_image_url(self, obj):
        return obj.profile_image_url if obj.profile_image_url else ''


class UserProfileV3Serializer(serializers.ModelSerializer):

    """
    Serializer for retrieving user profile details.
    """

    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    gender = serializers.CharField()
    oauth = serializers.SerializerMethodField()
    checkins = serializers.SerializerMethodField()
    points = serializers.CharField()
    image_url = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    stores = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'fname', 'lname','email','roles', 'phone', 'address','oauth', 'gender', 'checkins', 'points',
                  'image_url', 'dob', 'stores')

    def get_fname(self, obj):
        return '%s'%(obj.first_name)

    def get_lname(self, obj):
        return '%s'%(obj.last_name)

    def get_phone(self, obj):
        return '%s'%(obj.mobile) if obj.mobile else ''

    def get_roles(self, obj):
        return obj.roles.all().values_list('name', flat=True)

    def get_address(self, obj):
        return ""

    def get_dob(self, obj):
        return obj.dob.strftime('%d/%m/%Y') if obj.dob else ""

    def get_oauth(self, obj):
        as_fb_user = SocialAccount.objects.filter(user_id= obj.id, provider='facebook')
        as_gp_user = SocialAccount.objects.filter(user_id= obj.id, provider='google')
        return {
            'facebook':as_fb_user.count() > 0,
            'google':as_gp_user.count() > 0
        }

    def get_image_url(self, obj):
        return obj.profile_image_url if obj.profile_image_url else ''


class UserProfileUpdateSerializer(serializers.Serializer):

    """
    Serializer for editing user profile details.
    """

    fname = serializers.CharField()
    lname = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    def validate_password(self, value):
        request = self.context.get('request', None)
        password = value
        is_same_password = check_password(password, request.user.password)
        if is_same_password:
            raise serializers.ValidationError('You cannot use current password. Please try another.')
        return password

    def validate_email(self, value):
        request = self.context.get('request', None)
        if not value == request.user.email:
            try:
                User.objects.get(email=value)
                raise serializers.ValidationError('User with this email already exists.')
            except User.DoesNotExist:
                pass
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['fname']
        instance.last_name = validated_data['lname']
        instance.email = validated_data['email']
        instance.mobile = validated_data['phone']
        password = validated_data.get('password')
        if validated_data.get('password'):
            instance.set_password(password)
        instance.save()


class UserProfileUpdateV2Serializer(serializers.Serializer):

    """
    Serializer for editing user profile details.
    """

    fname = serializers.CharField()
    lname = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    gender = serializers.CharField()
    dob = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    def validate_password(self, value):
        request = self.context.get('request', None)
        password = value
        is_same_password = check_password(password, request.user.password)
        if is_same_password:
            raise serializers.ValidationError('You cannot use current password. Please try another.')
        return password

    def validate_email(self, value):
        request = self.context.get('request', None)
        if not value == request.user.email:
            try:
                User.objects.get(email=value)
                raise serializers.ValidationError('User with this email already exists.')
            except User.DoesNotExist:
                pass
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['fname']
        instance.last_name = validated_data['lname']
        instance.email = validated_data['email']
        instance.mobile = validated_data['phone']
        instance.gender = validated_data.get('gender')
        password = validated_data.get('password')
        if validated_data.get('password'):
            instance.set_password(password)
        if validated_data.get('dob'):
            print 'hereeeee'
            instance.dob = datetime.datetime.strptime(validated_data.get('dob'), "%d/%m/%Y").date()
        instance.save()


class FBProfileSerializer(serializers.Serializer):

    """
    Serializer for editing user profile details.
    """

    fname = serializers.CharField()
    lname = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data['fname']
        instance.last_name = validated_data['lname']
        instance.email = validated_data['email']
        instance.mobile = validated_data['phone']
        instance.save()
