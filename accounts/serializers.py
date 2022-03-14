"""Accounts serializers"""
from rest_framework import serializers

from accounts.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        """Meta class"""
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_superuser', 'is_staff', 'is_active']

    def create(self, validated_data):
        """User create"""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            is_superuser=validated_data['is_superuser'],
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """User update"""
        for key in validated_data:
            if key not in ['password', ]:
                setattr(instance, key, validated_data[key])

        if validated_data.get('password', None):
            instance.set_password(validated_data.get('password', None))

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer class"""
    user = UserSerializer(read_only=True)
    img = serializers.ImageField()
    friends = UserSerializer(read_only=True, many=True)

    class Meta:
        """Meta class"""
        model = Profile
        fields = ['id', 'user', 'user_id', 'phone', 'address', 'city', 'state', 'zipcode', 'available', 'img',
                  'friends']
