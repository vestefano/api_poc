"""Accounts views"""
from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, User, Friend
from accounts.permissions import IsOwnerOrAdmin, IsOwnerOrFriendOrAdmin
from accounts.serializers import ProfileSerializer, UserSerializer, FriendsSerializer, AdminUserSerializer


# Users views
class ListUserApiView(ListAPIView):
    """User list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminListUserApiView(ListAPIView):
    """Admin user list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


class RetrieveUserApiView(RetrieveAPIView):
    """User list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrFriendOrAdmin,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminRetrieveUserApiView(RetrieveAPIView):
    """Admin user list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


class CreateUserApiView(CreateAPIView):
    """User create api view"""
    permission_classes = [permissions.AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminCreateUserApiView(CreateAPIView):
    """User create api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    permission_classes = [permissions.AllowAny, ]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


class UpdateUserApiView(RetrieveUpdateAPIView):
    """User update api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminUpdateUserApiView(RetrieveUpdateAPIView):
    """Admin user update api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


class DestroyUserApiView(RetrieveDestroyAPIView):
    """User destroy api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminDestroyUserApiView(RetrieveDestroyAPIView):
    """User destroy api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


# Profiles views
class ListProfileApiView(ListAPIView):
    """Profile list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RetrieveProfileApiView(RetrieveAPIView):
    """Profile list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrFriendOrAdmin,
    ]
    lookup_field = 'user_id'
    action = "retrieve"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CreateProfileApiView(CreateAPIView):
    """Profile create api view"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UpdateProfileApiView(RetrieveUpdateAPIView):
    """Profile update api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DestroyProfileApiView(RetrieveDestroyAPIView):
    """Profile delete api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ListCreateFriendApiView(ListCreateAPIView):
    """Friend list  and create api view"""
    queryset = Friend.objects.all()
    serializer_class = FriendsSerializer


class ShorterConnectionFriends(APIView):
    """Short connection friends view"""

    @staticmethod
    def get(request, uid, ouid):
        """
        Return a list of shorter connection friends
        :param uid: User id
        :param ouid: Other user id
        :param request: Request
        :return: List of shorter connection friends
        """

        uid_exists = User.objects.filter(pk=uid).exists()
        ouid_exists = User.objects.filter(pk=ouid).exists()

        if not uid_exists or not ouid_exists:
            raise Http404

        shorter_connection = Friend.shorter_connection_friends(user_id=uid, other_user_id=ouid)

        return Response(shorter_connection)
