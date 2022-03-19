"""Unit test for accounts utils"""
from django.test import TestCase
import mock

from accounts.utils import FriendsConnections


class FriendsConnectionsTest(TestCase):
    """Test for FriendsConnections"""

    def test_find_connections_are_friends(self):
        """Test _find_connections when the user is friend of the target user"""
        friends_connections = FriendsConnections()
        user = mock.Mock(is_friend=mock.Mock(return_value=True))

        with mock.patch('accounts.utils.User.objects.get', return_value=user):
            result = friends_connections._find_connections(1, 2)

        self.assertEqual(result, [1])

    def test_find_connections_when_are_not_friends_but_are_a_connection(self):
        """Test _find_connections hen the user isn't friend of the target user but are a connection friend"""
        friends_connections = FriendsConnections()
        user = mock.Mock(is_friend=mock.Mock(return_value=False))
        user_2 = mock.Mock(is_friend=mock.Mock(return_value=True))
        friends = mock.Mock(__iter__=mock.Mock(return_value=iter([3, 4, 5])), count=mock.Mock(return_value=3))
        values_list = mock.Mock(values_list=mock.Mock(return_value=friends))
        exclude_mock_2 = mock.Mock(exclude=mock.Mock(return_value=values_list))
        exclude_mock = mock.Mock(exclude=mock.Mock(return_value=exclude_mock_2))

        with mock.patch('accounts.utils.User.objects.get', side_effect=[user, user_2]), \
             mock.patch('accounts.utils.Friend.objects.filter', return_value=exclude_mock):
            result = friends_connections._find_connections(1, 2)

        self.assertEqual(result, [1, 3])

    def test_find_connections_when_are_not_friends_and_are_not_connection(self):
        """Test _find_connections hen the user isn't friend of the target user and aren't a connection friend"""
        friends_connections = FriendsConnections()
        user = mock.Mock(is_friend=mock.Mock(return_value=False))
        friends = mock.Mock(count=mock.Mock(return_value=0))
        values_list = mock.Mock(values_list=mock.Mock(return_value=friends))
        exclude_mock_2 = mock.Mock(exclude=mock.Mock(return_value=values_list))
        exclude_mock = mock.Mock(exclude=mock.Mock(return_value=exclude_mock_2))

        with mock.patch('accounts.utils.User.objects.get', return_value=user), \
             mock.patch('accounts.utils.Friend.objects.filter', return_value=exclude_mock):
            result = friends_connections._find_connections(1, 2)

        self.assertIsNone(result)

    def test_shorter_connection(self):
        """Test shorter_connection"""
        user = mock.Mock(user=mock.Mock(id=1))
        user_2 = mock.Mock(user=mock.Mock(id=3))
        user_3 = mock.Mock(user=mock.Mock(id=5))
        first_mock = mock.Mock(first=mock.Mock(side_effect=[user_3, user_2, user]))
        filter_mock = mock.Mock(filter=mock.Mock(return_value=first_mock))

        with mock.patch('accounts.utils.FriendsConnections._find_connections', return_value=[1, 3, 4, 5, ]), \
             mock.patch('accounts.utils.Friend.objects.filter', return_value=filter_mock):
            result = FriendsConnections.shorter_connection(1, 2)

        self.assertEqual(result, [3, 5])

    def test_shorter_connection_when_user_is_friend(self):
        """Test shorter_connection when user is friend of the target user"""
        user = mock.Mock(id=1)
        first_mock = mock.Mock(first=mock.Mock(return_value=mock.Mock(user=user)))
        filter_mock = mock.Mock(filter=mock.Mock(return_value=first_mock))

        with mock.patch('accounts.utils.FriendsConnections._find_connections', return_value=[1, ]), \
             mock.patch('accounts.utils.Friend.objects.filter', return_value=filter_mock):
            result = FriendsConnections.shorter_connection(1, 2)

        self.assertEqual(result, [])

    def test_shorter_connection_when_not_connections(self):
        """Test shorter_connection when user don't have connection with the target user"""

        with mock.patch('accounts.utils.FriendsConnections._find_connections', return_value=None):
            result = FriendsConnections.shorter_connection(1, 2)

        self.assertEqual(result, [])
