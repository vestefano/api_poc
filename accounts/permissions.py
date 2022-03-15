"""Accounts custom permissions"""

from rest_framework import permissions

from accounts.models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admin.
    """

    def has_object_permission(self, request, view, obj):
        """Allow admin and owners"""
        user_request = request.user

        if user_request.is_superuser:
            return True
        elif isinstance(obj, User):
            return obj == user_request
        elif hasattr(obj, 'user'):
            return obj.user == user_request
        else:
            return False


class IsOwnerOrFriendOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admin.
    """

    def has_object_permission(self, request, view, obj):
        """Allow admin and owners"""
        user_request = request.user

        if user_request.is_superuser:
            return True
        elif isinstance(obj, User):
            return obj == user_request or user_request.is_friend(obj.id)
        elif hasattr(obj, 'user'):
            return obj.user == user_request or user_request.is_friend(obj.user.id)
        else:
            return False
