"""Accounts views"""
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView

from accounts.models import Profile
from accounts.serializers import ProfileSerializer


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


class RetrieveShorterConnectionFriend(APIView):
    """Shorter Connection Friend api view"""

    def get_shorter_connection(self):
        """Get shorter connection"""
        try:
            user_id = self.kwargs.get('pk')
            friend_id = self.kwargs.get('pk_friend')

            user = Profile.objects.filter(pk=user_id)
            friend = Profile.objects.filter(pk=friend_id)

            shorter_connection = Profile.objects.filter(friends=user).filter(friends=friend)

            serializer = ProfileSerializer(shorter_connection)

            return serializer

        except Profile.DoesNotExist:
            raise NotFound
