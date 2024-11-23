"""Integration test for views"""
import json
from unittest import skipIf

from django.conf import settings
from django.test import skipIfDBFeature
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from snapshottest.django import TestCase

from accounts.models import User, Profile, Friend


def get_request_credentials(user):
    """Add the JWT to header for request"""
    refresh = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'}


@skipIfDBFeature('is_mocked')
class UserApiViewsTest(TestCase):
    """Test for UserApiViews"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='JD2022',
            first_name='Jhon',
            last_name='Doe',
            email='jhon@example.com',
            password='top_secret!',
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

    @skipIf(settings.GITHUB_WORKFLOW, "The snapshot data not have the same id, because of that fail")
    def test_owner_retrieve_account(self):
        """Test user retrieve her details"""
        user = self.user
        url = reverse('account_retrieve_update_delete', args=[user.id])

        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertMatchSnapshot(data)

    def test_user_retrieve_details_of_another_account(self):
        """Test user retrieve details of another account"""
        user = self.user

        other_user = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                                email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                is_active=True)

        url = reverse('account_retrieve_update_delete', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_create_user(self):
        """Test create user"""
        url = reverse('account_create')
        body = {
            "username": "Alberto1215",
            "first_name": "Alberto",
            "last_name": "Small",
            "email": "albr@emali.com",
            "password": "top_secret!",
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['username'], body['username'])

    def test_update_user(self):
        """Test user update her own account"""
        user = self.user
        url = reverse('account_retrieve_update_delete', args=[user.id])

        body = {
            "username": "Mathias2021",
            "first_name": "Mathias",
            "last_name": "Doe",
            "email": "mathias@email.com",
            "password": "top_secret!",
        }

        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        user.refresh_from_db()
        self.assertEqual(body['username'], user.username)
        self.assertEqual(data['username'], user.username)

    def test_user_admin_update_another_account(self):
        """Test user admin update another account"""
        user = self.user
        user.is_superuser = True
        user.save()

        other_user = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                                email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                is_active=True)

        body = {
            "username": "Martha22",
            "first_name": "Martha",
            "last_name": "Doe",
            "email": "martha@email.com",
        }

        url = reverse('account_retrieve_update_delete', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        other_user.refresh_from_db()
        self.assertEqual(body['username'], other_user.username)
        self.assertEqual(data['username'], other_user.username)

    def test_user_try_update_another_account(self):
        """Test user try to update another account"""
        user = self.user
        other_user = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                                email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                is_active=True)

        body = {
            "username": "Martha22",
            "first_name": "Martha",
            "last_name": "Doe",
            "email": "martha@email.com",
        }

        url = reverse('account_retrieve_update_delete', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(body['username'], other_user.username)

    def test_delete_user(self):
        """Test user delete her own account"""
        user = self.user
        username = user.username

        url = reverse('account_retrieve_update_delete', args=[user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(username=username).exists())

    def test_user_admin_delete_another_account(self):
        """Test user admin delete another account"""
        user = self.user
        user.is_superuser = True
        user.save()

        other_user = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                                email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                is_active=True)
        username = other_user.username

        url = reverse('account_retrieve_update_delete', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(username=username).exists())

    def test_user_try_delete_another_account(self):
        """Test user try to delete another account"""
        user = self.user

        other_user = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                                email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                is_active=True)
        username = other_user.username

        url = reverse('account_retrieve_update_delete', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(username=username).exists())


@skipIfDBFeature('is_mocked')
class AdminUserApiViewsTest(TestCase):
    """Test for AdminUserApiViews"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='JD2022',
            first_name='Jhon',
            last_name='Doe',
            email='jhon@example.com',
            password='top_secret!',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

    @skipIf(settings.GITHUB_WORKFLOW, "The snapshot data not have the same id, because of that fail")
    def test_list_users(self):
        """Test list users endpoint"""
        user = self.user

        baker.make(User, username='Martha96', first_name='Martha', last_name='Doe', email='martha@example.com',
                   password='top_secret!', is_superuser=False, is_staff=False, is_active=True)

        baker.make(User, username='Mikael564', first_name='Mikael', last_name='Sans', email='mikael@example.com',
                   password='top_secret!', is_superuser=True, is_staff=True, is_active=True)

        url = reverse('account_manager_list')
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertMatchSnapshot(data)

    def test_create_user(self):
        """Test admin create user"""
        user = self.user
        body = {
            "username": "Alberto1215",
            "first_name": "Alberto",
            "last_name": "Small",
            "email": "albr@emali.com",
            "password": "top_secret!",
            "is_superuser": True,
            "is_active": True,
        }
        url = reverse('account_create')

        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['username'], body['username'])

    def test_admin_update_another_account(self):
        """Test user admin update another account"""
        user = self.user

        other_user = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                                email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                is_active=True)

        body = {
            "username": "Martha22",
            "first_name": "Martha",
            "last_name": "Doe",
            "email": "martha@email.com",
            "is_superuser": True,
        }

        url = reverse('account_manager_update', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        other_user.refresh_from_db()
        self.assertEqual(body['username'], other_user.username)
        self.assertEqual(data['username'], other_user.username)
        self.assertTrue(other_user.is_superuser)

    def test_admin_delete_another_account(self):
        """Test user admin delete another account"""
        user = self.user

        other_user = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                                email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                is_active=True)
        username = other_user.username

        url = reverse('account_manager_delete', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(username=username).exists())


@skipIfDBFeature('is_mocked')
class ProfilesApiViewsTest(TestCase):
    """Test for ProfilesApiViews"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='JD2022',
            first_name='Jhon',
            last_name='Doe',
            email='jhon@example.com',
            password='top_secret!',
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

    @skipIf(settings.GITHUB_WORKFLOW, "The snapshot data not have the same id, because of that fail")
    def test_list_profile(self):
        """Test list profiles"""
        user = self.user

        user_1 = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                            email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                            is_active=True)

        user_2 = baker.make(User, username='Mikael564', first_name='Mikael', last_name='Sans',
                            email='mikael@example.com', password='top_secret!', is_superuser=True, is_staff=True,
                            is_active=True)

        # Profiles
        baker.make(Profile, user=user, phone='(925)-967-1402', address='8655 Frances Ct', city='Paris', state='FR',
                   zipcode='65487', available=True, img='https://randomuser.me/api/portraits/women/65.jpg')

        baker.make(Profile, user=user_1, phone='(463)-159-7835', address='1401 Oak Lawn Ave', city='Canada', state='CD',
                   zipcode='98752', available=False, img='https://randomuser.me/api/portraits/women/56.jpg')

        baker.make(Profile, user=user_2, phone='(709)-501-3504', address='8909 Walnut Hill Ln', city='Mexico',
                   state='MX', zipcode='85245', available=True, img='https://randomuser.me/api/portraits/women/56.jpg')

        # Friends
        baker.make(Friend, user=user, is_friend_of=user_1)

        baker.make(Friend, user=user, is_friend_of=user_2)

        baker.make(Friend, user=user_1, is_friend_of=user_2)

        baker.make(Friend, user=user_2, is_friend_of=user)

        url = reverse('profile_list')
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertMatchSnapshot(data)

    def test_create_profile(self):
        """Test create profile"""
        user = self.user

        body = {
            "phone": "(463)-159-7835",
            "address": "1401 Oak Lawn Ave",
            "city": "Canada",
            "state": "CD",
            "zipcode": "65478",
            "img": "https://randomuser.me/api/portraits/women/56.jpg"
        }

        url = reverse('profile_create')
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(user.profile, Profile)

    def test_update_profile(self):
        """Test update profile"""
        user = self.user

        # Profiles
        baker.make(Profile, user=user, phone='(925)-967-1402', address='8655 Frances Ct', city='Paris', state='FR',
                   zipcode='65487', available=True, img='https://randomuser.me/api/portraits/women/65.jpg')

        body = {
            "city": "Oslo",
            "state": 'OL'
        }

        url = reverse('profile_update', args=[user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        profile = user.profile
        self.assertEqual(profile.city, body['city'])
        self.assertEqual(profile.state, body['state'])

    def test_admin_update_user_profile(self):
        """Test admin update an user profile"""
        user = self.user
        user.is_superuser = True
        user.save()

        user_1 = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                            email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                            is_active=True)

        # Profiles
        baker.make(Profile, user=user_1, phone='(925)-967-1402', address='8655 Frances Ct', city='Paris', state='FR',
                   zipcode='65487', available=True, img='https://randomuser.me/api/portraits/women/65.jpg')

        body = {
            "city": "Oslo",
            "state": 'OL'
        }

        url = reverse('profile_update', args=[user_1.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 200)
        user_1.refresh_from_db()
        profile = user_1.profile
        self.assertEqual(profile.city, body['city'])
        self.assertEqual(profile.state, body['state'])

    def test_user_try_update_another_user_profile(self):
        """Test user try update another user profile"""
        user = self.user

        user_1 = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                            email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                            is_active=True)

        # Profiles
        baker.make(Profile, user=user_1, phone='(925)-967-1402', address='8655 Frances Ct', city='Paris', state='FR',
                   zipcode='65487', available=True, img='https://randomuser.me/api/portraits/women/65.jpg')

        body = {
            "city": "Oslo",
            "state": 'OL'
        }

        url = reverse('profile_update', args=[user_1.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 403)
        user_1.refresh_from_db()
        profile = user_1.profile
        self.assertEqual(profile.city, 'Paris')
        self.assertEqual(profile.state, 'FR')

    def test_delete_profile(self):
        """Test delete profile"""
        user = self.user

        baker.make(Profile, user=user, phone='(925)-967-1402', address='8655 Frances Ct', city='Paris', state='FR',
                   zipcode='65487', available=True, img='https://randomuser.me/api/portraits/women/65.jpg')

        url = reverse('profile_delete', args=[user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Profile.objects.filter(user=user).exists())

    def test_admin_delete_profile(self):
        """Test admin delete a user profile"""
        user = self.user
        user.is_superuser = True
        user.save()

        user_1 = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                            email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                            is_active=True)

        # Profiles
        baker.make(Profile, user=user_1, phone='(925)-967-1402', address='8655 Frances Ct', city='Paris', state='FR',
                   zipcode='65487', available=True, img='https://randomuser.me/api/portraits/women/65.jpg')

        url = reverse('profile_delete', args=[user_1.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Profile.objects.filter(user=user_1).exists())

    def test_user_try_delete_profile(self):
        """Test user try delete a user profile"""
        user = self.user

        user_1 = baker.make(User, username='Martha96', first_name='Martha', last_name='Doe',
                            email='martha@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                            is_active=True)

        # Profiles
        baker.make(Profile, user=user_1, phone='(925)-967-1402', address='8655 Frances Ct', city='Paris', state='FR',
                   zipcode='65487', available=True, img='https://randomuser.me/api/portraits/women/65.jpg')

        url = reverse('profile_delete', args=[user_1.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Profile.objects.filter(user=user_1).exists())


@skipIfDBFeature('is_mocked')
class FriendsApiViewsTest(TestCase):
    """Test for Friends views"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()

        # Test users
        self.user_roberto = baker.make(User, username='Roberto646', first_name='Roberto', last_name='Doe',
                                       email='martha@example.com', password='top_secret!', is_superuser=True,
                                       is_staff=True, is_active=True)

        self.user_ana = baker.make(User, username='Ana564', first_name='Ana', last_name='Sans',
                                   email='mikael@example.com', password='top_secret!', is_superuser=False,
                                   is_staff=False, is_active=True)

        self.user_juan = baker.make(User, username='Juan564', first_name='Juan', last_name='Sans',
                                    email='mikael@example.com', password='top_secret!', is_superuser=False,
                                    is_staff=False, is_active=True)

        self.user_maykel = baker.make(User, username='Maykel564', first_name='Maykel', last_name='Sans',
                                      email='mikael@example.com', password='top_secret!', is_superuser=False,
                                      is_staff=False, is_active=True)

        self.user_leo = baker.make(User, username='Leo564', first_name='Leo', last_name='Sans',
                                   email='mikael@example.com', password='top_secret!', is_superuser=False,
                                   is_staff=False, is_active=True)

        # Test profiles
        baker.make(Profile, user=self.user_roberto, phone='(925)-967-1402', address='8655 Frances Ct',
                   city='France', state='FR', zipcode='65487', available=True,
                   img='https://randomuser.me/api/portraits/women/65.jpg')

        baker.make(Profile, user=self.user_ana, phone='(390)-568-1958', address='3494 Sunset St', city='Italy',
                   state='IT', zipcode='65487', available=True,
                   img='https://randomuser.me/api/portraits/women/65.jpg')

        baker.make(Profile, user=self.user_juan, phone='(396)-158-3397', address='4738 Fairview St', city='Poland',
                   state='PL', zipcode='65487', available=True,
                   img='https://randomuser.me/api/portraits/women/65.jpg')

        baker.make(Profile, user=self.user_maykel, phone='(438)-527-4225', address='8794 E Sandy Lake Rd',
                   city='Belarus', state='BL', zipcode='65487', available=True,
                   img='https://randomuser.me/api/portraits/women/65.jpg')

        baker.make(Profile, user=self.user_leo, phone='(750)-453-6615', address='1138 Valley View Ln',
                   city='Panama', state='PN', zipcode='65487', available=True,
                   img='https://randomuser.me/api/portraits/women/65.jpg')

    def friend_list_create(self):
        """Helper method for create users relations"""
        url = reverse('friend_list_create')

        body = {
            "user": self.user_roberto.id,
            "is_friend_of": self.user_ana.id,
        }

        http_auth = get_request_credentials(self.user_roberto)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user_roberto.is_friend(self.user_ana))

        body = {
            "user": self.user_roberto.id,
            "is_friend_of": self.user_juan.id,
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user_roberto.is_friend(self.user_juan))

        body = {
            "user": self.user_juan.id,
            "is_friend_of": self.user_maykel.id,
        }

        http_auth = get_request_credentials(self.user_juan)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user_juan.is_friend(self.user_maykel))

        body = {
            "user": self.user_maykel.id,
            "is_friend_of": self.user_leo.id,
        }

        http_auth = get_request_credentials(self.user_maykel)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user_maykel.is_friend(self.user_leo))

        body = {
            "user": self.user_ana.id,
            "is_friend_of": self.user_leo.id,
        }

        http_auth = get_request_credentials(self.user_ana)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user_ana.is_friend(self.user_leo))

    def test_create_friends(self):
        """Test create friends"""
        self.friend_list_create()

    @skipIf(settings.GITHUB_WORKFLOW, "The snapshot data not have the same id, because of that fail")
    def test_user_friends_profiles_list(self):
        """Test user friends profiles list """
        self.friend_list_create()

        url = reverse('friends_profiles', args=[self.user_roberto.id])
        http_auth = get_request_credentials(self.user_roberto)
        self.client.credentials(**http_auth)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertMatchSnapshot(data)

    def test_shorter_connection(self):
        """Test shorter connection between two users"""
        self.friend_list_create()

        url = reverse('shorter_connection_friends', args=[self.user_roberto.id, self.user_leo.id])
        http_auth = get_request_credentials(self.user_roberto)
        self.client.credentials(**http_auth)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], self.user_ana.id)

    def test_delete_friendship(self):
        """Test delete friendship"""
        self.friend_list_create()

        url = reverse('friendship_delete', args=[self.user_roberto.id, self.user_juan.id])
        http_auth = get_request_credentials(self.user_roberto)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(self.user_roberto.is_friend(self.user_juan.id))
