"""Accounts views"""
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView

from accounts.models import Profile, User, Friend
from accounts.serializers import ProfileSerializer, UserSerializer, FriendsSerializer


# Users views
class ListUserApiView(ListAPIView):
    """User list api view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserApiView(CreateAPIView):
    """User create api view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateUserApiView(UpdateAPIView):
    """User update api view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateUserApiView(RetrieveUpdateAPIView):
    """User retrieve and update api view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DestroyUserApiView(DestroyAPIView):
    """User destroy api view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Profiles views
class ListProfileApiView(ListAPIView):
    """Profile list api view"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RetrieveProfileApiView(RetrieveAPIView):
    """Profile list api view"""
    lookup_field = 'user_id'
    action = "retrieve"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CreateProfileApiView(CreateAPIView):
    """Profile create api view"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UpdateProfileApiView(UpdateAPIView):
    """Profile update api view"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RetrieveUpdateProfileApiView(RetrieveUpdateAPIView):
    """Profile retrieve and update api view"""
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
        :param ouid:
        :param uid:
        :param request: Request
        :return: List of shorter connection friends
        """

        uid_exists = User.objects.filter(pk=uid).exists()
        ouid_exists = User.objects.filter(pk=ouid).exists()

        if not uid_exists or not ouid_exists:
            raise Http404

        shorter_connection = Friend.shorter_connection_friends(user_id=uid, other_user_id=ouid)

        return Response(shorter_connection)
