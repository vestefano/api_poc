"""Accounts views"""
from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, User, Friend
from accounts.permissions import IsOwnerOrAdmin
from accounts.serializers import ProfileSerializer, UserSerializer, FriendsSerializer, AdminUserSerializer, \
    FriendsProfileSerializer
from accounts.utils import FriendsConnections


# Users views
class CreateUserApiView(CreateAPIView):
    """User create api view"""
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateDeleteUserApiView(RetrieveUpdateDestroyAPIView):
    """User retrieve, update and delete api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Admin user views
class AdminListCreateUserApiView(ListCreateAPIView):
    """Admin user list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


class AdminRetrieveUpdateDeleteUserApiView(RetrieveUpdateDestroyAPIView):
    """Admin user update api view"""
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
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CreateProfileApiView(CreateAPIView):
    """Profile create api view"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RetrieveProfileApiView(RetrieveAPIView):
    """Profile list api view"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = 'user_id'
    action = "retrieve"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UpdateProfileApiView(RetrieveUpdateAPIView):
    """Profile update api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    lookup_field = 'user_id'
    action = "retrieve"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DestroyProfileApiView(RetrieveDestroyAPIView):
    """Profile delete api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    lookup_field = 'user_id'
    action = "retrieve"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Friends views
class ListCreateFriendApiView(ListCreateAPIView):
    """Friend list  and create api view"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Friend.objects.all()
    serializer_class = FriendsSerializer


class RetrieveFriendsApiView(RetrieveAPIView):
    """Retrieve user friends profiles"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = 'user_id'
    action = "retrieve"
    queryset = Profile.objects.all()
    serializer_class = FriendsProfileSerializer


class DeleteFriendshipAPIView(DestroyAPIView):
    """Delete friendship api view"""
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin,
    ]
    queryset = Friend.objects.all()
    serializer_class = FriendsSerializer

    def get_object(self):
        """Get object"""
        queryset = self.get_queryset()
        filters = {
            'user_id': self.kwargs['user_id'],
            'is_friend_of': self.kwargs['friend_id'],
        }
        obj = get_object_or_404(queryset, **filters)
        self.check_object_permissions(self.request, obj)
        return obj


class ShorterConnectionFriends(APIView):
    """Short connection friends view"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    def get(request, uid, ouid):
        """
        Return a list of shorter connection friends
        :param request: Request
        :param uid: User id
        :param ouid: Other user id
        :return: List of shorter connection friends
        """
        shorter_connection = []

        if uid == ouid:
            return Response(shorter_connection)

        uid_exists = User.objects.filter(pk=uid).exists()
        ouid_exists = User.objects.filter(pk=ouid).exists()

        if not uid_exists or not ouid_exists:
            raise Http404

        shorter_connection = FriendsConnections.shorter_connection(user_id=uid, other_user_id=ouid)

        return Response(shorter_connection)
