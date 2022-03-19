from django.http import Http404
from django.test import TestCase
import mock

from accounts.views import ShorterConnectionFriends, DeleteFriendshipAPIView


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

    def test_get_when_send_same_ids(self):
        """Test get when send the same ids"""
        response = mock.Mock()
        with mock.patch('accounts.views.Response', return_value=response):
            shorter_connection = ShorterConnectionFriends.get(mock.Mock(), 1, 1)

        self.assertEqual(shorter_connection, response)


class DeleteFriendshipAPIViewTest(TestCase):
    """Test DeleteFriendshipAPIView"""

    def test_get_object(self):
        """Test get_object"""
        kwargs = {
            'user_id': 1,
            'friend_id': 2
        }
        delete_view = mock.Mock(kwargs=kwargs, get_queryset=mock.Mock(), check_object_permissions=mock.Mock())
        obj = mock.Mock()

        with mock.patch('accounts.views.get_object_or_404', return_value=obj):
            result = DeleteFriendshipAPIView.get_object(delete_view)

        self.assertEqual(result, obj)
