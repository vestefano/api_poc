"""Accounts serializers"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.models import User, Profile, Friend

INVALID_CODE = 400
FIELD_NOT_EMPTY = _('This field may not be blank.')
INVALID_USER = _('This user already has a profile or is not authenticated')


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    password = serializers.CharField(required=False, write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        """Meta class"""
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        """User create"""
        if not validated_data.get('password', None):
            raise serializers.ValidationError({'password': [FIELD_NOT_EMPTY]}, code=INVALID_CODE)

        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_superuser=False,
            is_staff=False,
            is_active=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """User update"""
        for key in validated_data:
            if key != 'password':
                setattr(instance, key, validated_data[key])

        if validated_data.get('password', None):
            instance.set_password(validated_data.get('password', None))

        instance.save()
        return instance


class AdminUserSerializer(serializers.ModelSerializer):
    """Admin user serializer"""

    password = serializers.CharField(required=False, write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(initial=True)

    class Meta:
        """Meta class"""
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_superuser', 'is_active']

    def create(self, validated_data):
        """User create"""
        if not validated_data.get('password', None):
            raise serializers.ValidationError({'password': [FIELD_NOT_EMPTY]}, code=INVALID_CODE)

        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_superuser=validated_data['is_superuser'],
            is_staff=validated_data['is_superuser'],
            is_active=validated_data['is_active']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """User update"""
        for key in validated_data:
            if key != 'password':
                setattr(instance, key, validated_data[key])

        if validated_data.get('password', None):
            instance.set_password(validated_data.get('password', None))

        instance.save()
        return instance


class FriendsSerializer(serializers.ModelSerializer):
    """Friends serializer class"""

    class Meta:
        """Meta class"""
        model = Friend
        fields = ['user', 'is_friend_of']


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer class"""
    friends = serializers.ListField(read_only=True, source='get_user_friends')
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    available = serializers.BooleanField(read_only=True, initial=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')

    class Meta:
        """Meta class"""
        model = Profile
        fields = ['user_id', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zipcode',
                  'available', 'friends', 'img']

    def create(self, validated_data):
        """Profile create"""
        request = self.context['request']

        if not request.user.id or Profile.objects.filter(user_id=request.user.id).exists():
            raise serializers.ValidationError({"user": [INVALID_USER]}, code=INVALID_CODE)

        profile = Profile(user_id=request.user.id, **validated_data)
        profile.save()
        return profile
