"""Accounts models"""
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser, PermissionsMixin):
    """User model"""

    @property
    def friends_id_list(self):
        """Friends id list"""
        return Friend.get_friends_id_list(self.id)

    def is_friend(self, possible_friend_id):
        """Is user friend of possible_friend_id"""
        return Friend.are_friends(self.id, possible_friend_id)


class Profile(models.Model):
    """Profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', help_text='Related user')
    phone = models.CharField(max_length=15, blank=True, unique=True, null=True, help_text='Phone field')
    address = models.CharField(max_length=100, blank=True, null=True, help_text='Address field')
    city = models.CharField(max_length=100, blank=True, null=True, help_text='City field')
    state = models.CharField(max_length=2, blank=True, null=True, help_text='State field')
    zipcode = models.CharField(max_length=10, blank=True, null=True, help_text='Zipcode field')
    available = models.BooleanField(default=True, help_text='User is available')
    img = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):  # pragma: no cover
        return self.user.username

    def get_user_friends_id(self):
        """Get user friends"""
        return self.user.friends_id_list

    def get_friends_profiles(self):
        """Get user friends"""
        return Profile.objects.filter(user_id__in=self.user.friends_id_list)


class Friend(models.Model):
    """Friends model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    is_friend_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_friend_of')

    class Meta:
        unique_together = ('user', 'is_friend_of',)

    @staticmethod
    def are_friends(user_id, possible_friend_id):
        """The user_id is friend of possible_friend_id"""
        return Friend.objects.filter(user_id=user_id).filter(is_friend_of=possible_friend_id).exists()

    @staticmethod
    def get_friends_id_list(user_id):
        """Friends ids of user_id"""
        return Friend.objects.filter(user_id=user_id).values_list('is_friend_of', flat=True)
