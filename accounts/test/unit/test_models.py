"""Unit test for accounts model"""
from django.test import TestCase
import mock

from accounts.models import Profile, User, Friend


class UserModelTest(TestCase):
    """Test for User Model"""

    def test_friends_id_list(self):
        """Test friends id list"""
        friends = mock.Mock()

        with mock.patch('accounts.models.Friend.get_friends_id_list', return_value=friends):
            user = User()
            result = user.friends_id_list

        self.assertEqual(friends, result)

    def test_is_friend(self):
        """Test is friend"""
        user = mock.Mock(spec=User, id=1)
        possible_friend = mock.Mock(spec=User, id=2)

        with mock.patch('accounts.models.Friend.are_friends', return_value=True):
            result = User.is_friend(user, possible_friend.id)

        self.assertTrue(result)


class ProfileModelTest(TestCase):
    """Test for Profile Model"""

    def test_get_user_fiends(self):
        """Test get user friends"""
        user_friends = mock.Mock()
        profile = mock.Mock(user=mock.Mock(friends_id_list=user_friends))

        result = Profile.get_user_friends(profile)

        self.assertEqual(user_friends, result)


class FriendModelTest(TestCase):
    """Test for Friend Model"""

    def test_are_friends(self):
        """Test for are_friends"""
        user = mock.Mock(spec=User, id=1)
        possible_friend = mock.Mock(spec=User, id=2)
        filter_mock = mock.Mock(filter=mock.Mock(return_value=mock.Mock(exists=mock.Mock(return_value=True))))

        with mock.patch('accounts.models.Friend.objects.filter', return_value=filter_mock):
            result = Friend.are_friends(user.id, possible_friend.id)

        self.assertTrue(result)

    def test_get_friends_id_list(self):
        """Test for get_friends_id_list"""
        user = mock.Mock(spec=User, id=1)
        friends_id_list = mock.Mock()
        values_list = mock.Mock(values_list=mock.Mock(return_value=friends_id_list))

        with mock.patch('accounts.models.Friend.objects.filter', return_value=values_list):
            result = Friend.get_friends_id_list(user.id)

        self.assertEqual(friends_id_list, result)
