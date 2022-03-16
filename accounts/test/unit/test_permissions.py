"""Unit test for permissions"""
from django.test import TestCase
import mock

from accounts.models import User
from accounts.permissions import IsOwnerOrAdmin, IsOwnerOrFriendOrAdmin


class IsOwnerOrAdminTest(TestCase):
    """Test for IsOwnerOrAdmin"""

    def test_has_object_permission_user_is_superuser(self):
        """Test for has_object_permission when user is superuser"""
        user = mock.Mock(spec=User, is_superuser=True)
        view = mock.Mock()
        obj = mock.Mock()
        request = mock.Mock(user=user)

        permission = IsOwnerOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        self.assertTrue(result)

    def test_has_object_permission_user_is_not_superuser_obj_is_user_instance(self):
        """Test for has_object_permission when user isn't superuser but obj is User instance and this user made the
        request """
        user = mock.Mock(spec=User, is_superuser=False)
        view = mock.Mock()
        obj = user
        request = mock.Mock(user=user)

        permission = IsOwnerOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        self.assertTrue(result)

    def test_has_object_permission_user_is_not_superuser_obj_is_not_user_instance(self):
        """Test for has_object_permission when user isn't superuser, obj isn't User instance but obj has a field called
         user and this user made the request"""
        user = mock.Mock(spec=User, is_superuser=False)
        view = mock.Mock()
        obj = mock.Mock(user=user)
        request = mock.Mock(user=user)

        permission = IsOwnerOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        self.assertTrue(result)

    def test_has_object_permission_user_does_not_have_permission(self):
        """Test for has_object_permission when user doesn't have permission"""
        user = mock.Mock(spec=User, is_superuser=False)
        view = mock.Mock()
        obj = mock.Mock()
        request = mock.Mock(user=user)

        permission = IsOwnerOrAdmin()
        with mock.patch('accounts.permissions.hasattr', return_value=False):
            result = permission.has_object_permission(request, view, obj)

        self.assertFalse(result)


class IsOwnerOrFriendOrAdminTest(TestCase):
    """Test for IsOwnerOrFriendOrAdmin"""

    def test_has_object_permission_user_is_superuser(self):
        """Test for has_object_permission when user is superuser"""
        user = mock.Mock(spec=User, is_superuser=True, is_friend=mock.Mock(return_value=False))
        view = mock.Mock()
        obj = mock.Mock()
        request = mock.Mock(user=user)

        permission = IsOwnerOrFriendOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        user.is_friend.assert_not_called()
        self.assertTrue(result)

    def test_has_object_permission_user_is_not_superuser_obj_is_user_instance(self):
        """Test for has_object_permission when user isn't superuser but obj is User instance and this user made the
        request """
        user = mock.Mock(spec=User, is_superuser=False, is_friend=mock.Mock(return_value=False))
        view = mock.Mock()
        obj = user
        request = mock.Mock(user=user)

        permission = IsOwnerOrFriendOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        user.assert_not_called()
        self.assertTrue(result)

    def test_has_object_permission_user_is_not_superuser_obj_is_user_instance_and_friend_of_requester(self):
        """Test for has_object_permission when user isn't superuser but obj is User instance and this request user is
        friend of obj user"""
        user = mock.Mock(spec=User, is_superuser=False, is_friend=mock.Mock(return_value=True))
        view = mock.Mock()
        obj = mock.Mock(spec=User)
        request = mock.Mock(user=user)

        permission = IsOwnerOrFriendOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        user.is_friend.assert_called_once_with(obj.id)
        self.assertTrue(result)

    def test_has_object_permission_user_is_not_superuser_obj_is_not_user_instance(self):
        """Test for has_object_permission when user isn't superuser, obj isn't User instance but obj has a field called
         user and this user made the request"""
        user = mock.Mock(spec=User, is_superuser=False, is_friend=mock.Mock(return_value=False))
        view = mock.Mock()
        obj = mock.Mock(user=user)
        request = mock.Mock(user=user)

        permission = IsOwnerOrFriendOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        user.is_friend.assert_not_called()
        self.assertTrue(result)

    def test_has_object_permission_user_is_not_superuser_obj_is_not_user_instance_user_owner_of_obj_is_friend(self):
        """Test for has_object_permission when user isn't superuser, obj isn't User instance but obj has a field called
         user, user that made the request is friend of obj owner user"""
        user = mock.Mock(spec=User, is_superuser=False, is_friend=mock.Mock(return_value=True))
        view = mock.Mock()
        obj = mock.Mock(user=mock.Mock(spec=User))
        request = mock.Mock(user=user)

        permission = IsOwnerOrFriendOrAdmin()
        result = permission.has_object_permission(request, view, obj)

        user.is_friend.assert_called_once_with(obj.user.id)
        self.assertTrue(result)

    def test_has_object_permission_user_does_not_have_permission(self):
        """Test for has_object_permission when user doesn't have permission"""
        user = mock.Mock(spec=User, is_superuser=False, is_friend=mock.Mock(return_value=False))
        view = mock.Mock()
        obj = mock.Mock()
        request = mock.Mock(user=user)

        permission = IsOwnerOrFriendOrAdmin()
        with mock.patch('accounts.permissions.hasattr', return_value=False):
            result = permission.has_object_permission(request, view, obj)

        user.is_friend.assert_not_called()
        self.assertFalse(result)
