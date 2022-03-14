"""Accounts serializers"""
from rest_framework import serializers

from accounts.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        """Meta class"""
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_superuser', 'is_staff',
                  'is_active']

    def create(self, validated_data):
        """User create"""
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
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
    # img = serializers.ImageField(use_url=True)
    friends = UserSerializer(many=True, read_only=True)

    class Meta:
        """Meta class"""
        model = Profile
        fields = ['id', 'user', 'phone', 'address', 'city', 'state', 'zipcode', 'available', 'friends']
