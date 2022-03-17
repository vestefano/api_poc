"""Integration test for views"""
import json
from django.urls import reverse
from django.test import skipIfDBFeature
from snapshottest.django import TestCase
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User, Profile, Friend


def get_request_credentials(user):
    """Add the JWT to header for request"""
    refresh = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'}


@skipIfDBFeature('is_mocked')
class UserApiViewsTest(TestCase):
    """Test for UserApiViews"""

    def setUp(self):
        super(UserApiViewsTest, self).setUp()
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

    def test_list_users(self):
        """Test list users endpoint"""
        user = self.user

        baker.make(User, username='Martha96', first_name='Martha', last_name='Doe', email='martha@example.com',
                   password='top_secret!', is_superuser=False, is_staff=False, is_active=True)

        baker.make(User, username='Mikael564', first_name='Mikael', last_name='Sans', email='mikael@example.com',
                   password='top_secret!', is_superuser=True, is_staff=True, is_active=True)

        url = reverse('account_list')
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertMatchSnapshot(data)

    def test_owner_retrieve_account(self):
        """Test user retrieve her details"""
        user = self.user
        url = reverse('account_details', args=[user.id])

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

        url = reverse('account_details', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertMatchSnapshot(data)

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
        url = reverse('account_update', args=[user.id])

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

        url = reverse('account_update', args=[other_user.id])
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

        url = reverse('account_update', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(body['username'], other_user.username)

    def test_delete_user(self):
        """Test user delete her own account"""
        user = self.user
        username = user.username

        url = reverse('account_delete', args=[user.id])
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

        url = reverse('account_delete', args=[other_user.id])
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

        url = reverse('account_delete', args=[other_user.id])
        http_auth = get_request_credentials(user)
        self.client.credentials(**http_auth)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(username=username).exists())


@skipIfDBFeature('is_mocked')
class AdminUserApiViewsTest(TestCase):
    """Test for AdminUserApiViews"""

    def setUp(self):
        super(AdminUserApiViewsTest, self).setUp()
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
        super(ProfilesApiViewsTest, self).setUp()
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
        super(FriendsApiViewsTest, self).setUp()
        self.client = APIClient()

    def test_list_profile(self):
        """Test list profiles"""

        user_roberto = baker.make(User, username='Roberto646', first_name='Roberto', last_name='Doe',
                                  email='martha@example.com', password='top_secret!', is_superuser=True,
                                  is_staff=True, is_active=True)

        user_ana = baker.make(User, username='Ana564', first_name='Ana', last_name='Sans',
                              email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                              is_active=True)

        user_juan = baker.make(User, username='Juan564', first_name='Juan', last_name='Sans',
                               email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                               is_active=True)

        user_maykel = baker.make(User, username='Maykel564', first_name='Maykel', last_name='Sans',
                                 email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                 is_active=True)

        user_leo = baker.make(User, username='Leo564', first_name='Leo', last_name='Sans',
                              email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                              is_active=True)

        url = reverse('friend_list_create')

        body = {
            "user": user_roberto.id,
            "is_friend_of": user_ana.id,
        }

        http_auth = get_request_credentials(user_roberto)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user_roberto.is_friend(user_ana))

        body = {
            "user": user_roberto.id,
            "is_friend_of": user_juan.id,
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user_roberto.is_friend(user_juan))

        body = {
            "user": user_juan.id,
            "is_friend_of": user_maykel.id,
        }

        http_auth = get_request_credentials(user_juan)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user_juan.is_friend(user_maykel))

        body = {
            "user": user_maykel.id,
            "is_friend_of": user_leo.id,
        }

        http_auth = get_request_credentials(user_maykel)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user_maykel.is_friend(user_leo))

        body = {
            "user": user_ana.id,
            "is_friend_of": user_leo.id,
        }

        http_auth = get_request_credentials(user_ana)
        self.client.credentials(**http_auth)
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user_ana.is_friend(user_leo))

    def test_shorter_connection(self):
        """Test shorter connection between two users"""
        user_roberto = baker.make(User, username='Roberto646', first_name='Roberto', last_name='Doe',
                                  email='martha@example.com', password='top_secret!', is_superuser=True,
                                  is_staff=True, is_active=True)

        user_ana = baker.make(User, username='Ana564', first_name='Ana', last_name='Sans',
                              email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                              is_active=True)

        user_juan = baker.make(User, username='Juan564', first_name='Juan', last_name='Sans',
                               email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                               is_active=True)

        user_maykel = baker.make(User, username='Maykel564', first_name='Maykel', last_name='Sans',
                                 email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                                 is_active=True)

        user_leo = baker.make(User, username='Leo564', first_name='Leo', last_name='Sans',
                              email='mikael@example.com', password='top_secret!', is_superuser=False, is_staff=False,
                              is_active=True)

        url = reverse('friend_list_create')

        body = {
            "user": user_roberto.id,
            "is_friend_of": user_ana.id,
        }

        http_auth = get_request_credentials(user_roberto)
        self.client.credentials(**http_auth)
        self.client.post(url, body)

        body = {
            "user": user_roberto.id,
            "is_friend_of": user_juan.id,
        }

        self.client.post(url, body)

        body = {
            "user": user_juan.id,
            "is_friend_of": user_maykel.id,
        }

        http_auth = get_request_credentials(user_juan)
        self.client.credentials(**http_auth)
        self.client.post(url, body)

        body = {
            "user": user_maykel.id,
            "is_friend_of": user_leo.id,
        }

        http_auth = get_request_credentials(user_maykel)
        self.client.credentials(**http_auth)
        self.client.post(url, body)

        body = {
            "user": user_ana.id,
            "is_friend_of": user_leo.id,
        }

        http_auth = get_request_credentials(user_ana)
        self.client.credentials(**http_auth)
        self.client.post(url, body)

        url = reverse('shorter_connection_friends', args=[user_roberto.id, user_leo.id])
        http_auth = get_request_credentials(user_roberto)
        self.client.credentials(**http_auth)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], user_ana.id)
