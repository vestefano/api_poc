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

        if isinstance(obj, User):
            return obj == user_request

        if hasattr(obj, 'user'):
            return obj.user == user_request

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

        if isinstance(obj, User):
            return obj == user_request or user_request.is_friend(obj.id)

        if hasattr(obj, 'user'):
            return obj.user == user_request or user_request.is_friend(obj.user.id)

        return False
