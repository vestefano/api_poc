"""Accounts models"""
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from cloudinary.models import CloudinaryField


class User(AbstractUser, PermissionsMixin):
    """User model"""
    pass


class Profile(models.Model):
    """Profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', help_text='Related user')
    phone = models.CharField(max_length=15, blank=True, unique=True, null=True, help_text='Phone field')
    address = models.CharField(max_length=100, blank=True, null=True, help_text='Address field')
    city = models.CharField(max_length=100, blank=True, null=True, help_text='City field')
    state = models.CharField(max_length=2, blank=True, null=True, help_text='State field')
    zipcode = models.CharField(max_length=10, blank=True, null=True, help_text='Zipcode field')
    available = models.BooleanField(default=True, help_text='User is available')
    img = CloudinaryField('img')

    def __str__(self):
        return self.username

    def get_user_friends(self):
        """Get user friends"""
        return self.user.user.values_list('is_friend_of')


class Friend(models.Model):
    """Friends model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    is_friend_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_friend_of')

    class Meta:
        unique_together = ('user', 'is_friend_of',)

    @staticmethod
    def shorter_connection_friends(user_id, other_user_id):
        """Shorter connection between users"""
        user_knows = Friend.objects.filter(user_id=user_id).values('is_friend_of')
        know_user = Friend.objects.filter(is_friend_of=other_user_id).values('user_id')
        return user_knows.intersection(know_user)
