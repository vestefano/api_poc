"""Accounts utils"""
from accounts.models import User, Friend


class FriendsConnections:
    """Class for friends connections operations"""

    @classmethod
    def _find_connections(cls, user_id, other_user_id):
        """
        Function for find possible connections between user and other_user
        :param user_id: Starting user id
        :param other_user_id: Final destination user id
        :return: A list or None is returned if there is no connection between users
        """
        users_visited = []  # List of ids of users who have already been visited
        connections_to_explore = [user_id, ]  # List of ids of the users that are missing to visit

        while connections_to_explore:

            visiting_user_id = connections_to_explore.pop(0)  # The first user in the list is extracted to go visit him
            users_visited.append(visiting_user_id)  # This user is passed to the visited list

            # The user to be visited is searched and it is asked if he is a direct friend of the final destination user
            user = User.objects.get(pk=visiting_user_id)
            if user.is_friend(other_user_id):
                return users_visited

            # If the user is not a direct friend of the final destination user, all his friends who are not in
            # the list of visited users or connections to visit are searched for, if he has friends that meet these
            # conditions they are added to the end of the list of connections to explore.
            friends = Friend.objects.filter(user_id=visiting_user_id).exclude(is_friend_of__in=users_visited). \
                exclude(is_friend_of__in=connections_to_explore).values_list('is_friend_of', flat=True)
            if friends.count() > 0:
                connections_to_explore.extend(friends)

    @classmethod
    def shorter_connection(cls, user_id, other_user_id):
        """Function for find the shorter connection between user and other_user"""
        shorter_connection = []
        target_id = other_user_id

        # They find the possible connection between the two users
        connections = cls._find_connections(user_id, other_user_id)

        if not connections:
            return shorter_connection

        # This is where the shortest connection is sought. This is built from the end user. The friend of the target
        # user found in the previously found connections is searched. Then this user is added to the shortest
        # connection and removed from the connections found. This is done until reaching the initial user.
        while target_id != user_id:
            target_id = Friend.objects.filter(is_friend_of=target_id).filter(user__in=connections).first().user.id
            shorter_connection.append(target_id)
            connections.remove(target_id)

        # The initial user of the shortest connection is removed. Since the path was built from the destination user
        # to the source user, the list is flipped.
        shorter_connection.remove(user_id)
        shorter_connection.reverse()

        return shorter_connection
