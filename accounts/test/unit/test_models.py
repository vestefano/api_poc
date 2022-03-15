"""Unit test for accounts model"""
from django.test import TestCase
import mock

from accounts.models import Profile


class ProfileModelTest(TestCase):
    """Test for Profile Model"""

    def test_get_user_fiends(self):
        """Test get user friends"""
        user_friends = mock.Mock()
        profile = mock.Mock(user=mock.Mock(user=mock.Mock(values_list=mock.Mock(return_value=user_friends))))

        result = Profile.get_user_friends(profile)

        self.assertEqual(user_friends, result)
