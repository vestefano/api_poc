"""Unit test for serializers"""
import mock
from django.test import TestCase
from rest_framework import serializers

from accounts.models import User, Profile
from accounts.serializers import UserSerializer, AdminUserSerializer, ProfileSerializer


class UserSerializerTest(TestCase):
    """Test for UserSerializer"""

    def test_create(self):
        """Test UserSerializer create"""
        user = mock.Mock(spec=User, set_password=mock.Mock(), save=mock.Mock())
        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
            'password': 'supersegura123',
        }

        with mock.patch('accounts.serializers.User', return_value=user):
            user_serializer = UserSerializer()
            result = user_serializer.create(validated_data)

        user.set_password.assert_called_once_with(validated_data['password'])
        user.save.assert_called_once()
        self.assertEqual(user, result)

    def test_create_without_password(self):
        """Test UserSerializer create without password"""
        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
        }
        user_serializer = UserSerializer()

        with self.assertRaises(serializers.ValidationError):
            user_serializer.create(validated_data)

    def test_update(self):
        """Test UserSerializer update"""
        user = mock.Mock(save=mock.Mock())

        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
        }

        user_serializer = UserSerializer()
        result = user_serializer.update(user, validated_data)

        user.save.assert_called_once()
        user.set_password.assert_not_called()
        self.assertEqual(user, result)

    def test_update_password(self):
        """Test UserSerializer update password"""
        user = mock.Mock(save=mock.Mock())

        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
            'password': 'supersegura123',
        }

        user_serializer = UserSerializer()
        result = user_serializer.update(user, validated_data)

        user.save.assert_called_once()
        user.set_password.assert_called_once_with(validated_data['password'])
        self.assertEqual(user, result)


class AdminUserSerializerTest(TestCase):
    """Test for AdminUserSerializer"""

    def test_create(self):
        """Test AdminUserSerializer create"""
        user = mock.Mock(spec=User, set_password=mock.Mock(), save=mock.Mock())
        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
            'password': 'supersegura123',
            'is_superuser': True,
            'is_active': True,
        }

        with mock.patch('accounts.serializers.User', return_value=user):
            admin_serializer = AdminUserSerializer()
            result = admin_serializer.create(validated_data)

        user.set_password.assert_called_once_with(validated_data['password'])
        user.save.assert_called_once()
        self.assertEqual(user, result)

    def test_create_without_password(self):
        """Test AdminUserSerializer create without password"""
        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
            'is_superuser': True,
            'is_active': True,
        }
        admin_serializer = AdminUserSerializer()

        with self.assertRaises(serializers.ValidationError):
            admin_serializer.create(validated_data)

    def test_update(self):
        """Test AdminUserSerializer update"""
        user = mock.Mock(save=mock.Mock())

        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
            'is_superuser': False,
            'is_active': True,
        }

        admin_serializer = AdminUserSerializer()
        result = admin_serializer.update(user, validated_data)

        user.save.assert_called_once()
        user.set_password.assert_not_called()
        self.assertEqual(user, result)

    def test_update_password(self):
        """Test AdminUserSerializer update password"""
        user = mock.Mock(save=mock.Mock())

        validated_data = {
            'username': 'JD',
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'jhon@email.com',
            'password': 'supersegura123',
            'is_superuser': True,
            'is_active': True,
        }

        admin_serializer = AdminUserSerializer()
        result = admin_serializer.update(user, validated_data)

        user.save.assert_called_once()
        user.set_password.assert_called_once_with(validated_data['password'])
        self.assertEqual(user, result)


class ProfileSerializerTest(TestCase):
    """Test for ProfileSerializer"""

    def test_create(self):
        """Test create"""
        user = mock.Mock(spec=User, id=1)
        profile = mock.Mock(spec=Profile, save=mock.Mock())
        profile_serializer = mock.Mock(spec=ProfileSerializer, context={'request': user})
        profile_exists = mock.Mock(exists=mock.Mock(return_value=False))

        with mock.patch('accounts.serializers.Profile', return_value=profile), \
             mock.patch('accounts.serializers.Profile.objects.filter', return_value=profile_exists):
            result = ProfileSerializer.create(profile_serializer, {})

        profile.save.assert_called_once()
        self.assertEqual(profile, result)

    def test_try_create_two_profiles(self):
        """Test try create two profile for same user"""
        user = mock.Mock(spec=User, id=1)
        profile = mock.Mock(spec=Profile, save=mock.Mock())
        profile_serializer = mock.Mock(spec=ProfileSerializer, context={'request': user})
        profile_exists = mock.Mock(exists=mock.Mock(return_value=True))

        with mock.patch('accounts.serializers.Profile', return_value=profile), \
             mock.patch('accounts.serializers.Profile.objects.filter', return_value=profile_exists), \
             self.assertRaises(serializers.ValidationError):
            ProfileSerializer.create(profile_serializer, {})

        profile.save.assert_not_called()
