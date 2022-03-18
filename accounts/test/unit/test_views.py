from django.http import Http404
from django.test import TestCase
import mock

from accounts.views import ShorterConnectionFriends


class ShorterConnectionFriendsTest(TestCase):
    """Test for ShorterConnectionFriends"""

    def test_get(self):
        """Test get happy path"""
        response = mock.Mock()
        exists = mock.Mock(return_value=True)

        with mock.patch('accounts.views.User.objects.filter', return_value=mock.Mock(exists=exists)), \
             mock.patch('accounts.views.FriendsConnections.shorter_connection', return_value=mock.Mock()), \
             mock.patch('accounts.views.Response', return_value=response):
            result = ShorterConnectionFriends.get(mock.Mock(), 1, 2)

        self.assertEqual(response, result)

    def test_get_fail(self):
        """Test get with the fail path"""
        exists = mock.Mock(return_value=False)

        with mock.patch('accounts.views.User.objects.filter', return_value=mock.Mock(exists=exists)), \
             mock.patch('accounts.views.FriendsConnections.shorter_connection', return_value=mock.Mock()), \
             self.assertRaises(Http404):
            ShorterConnectionFriends.get(mock.Mock(), 1, 2)
