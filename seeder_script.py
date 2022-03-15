"""Seeder script for fill the DB"""
import json
import random
import tempfile

from urllib.request import urlopen
from PIL import Image

import requests
from randomuser import RandomUser

API_URL = 'http://localhost:8000'


def create_users(users_amount):
    """
    This function create the users and booking in the rest api
    :param users_amount: Number of users you want to generate
    :return: None
    """
    try:
        users = RandomUser.generate_users(users_amount)
        api_user_create_url = API_URL + '/api/user/create/'
        api_profile_create_url = API_URL + '/api/profile/create/'

        for user in users:
            is_admin = random.choice(['true', 'false'])
            is_staff = random.choice(['true', 'false'])

            # Create User
            user_data = {
                "username": user.get_username(),
                "first_name": user.get_first_name(),
                "last_name": user.get_last_name(),
                "email": user.get_email(),
                "password": user.get_password(),
                "is_superuser": is_admin,
                "is_staff": is_staff,
                "is_active": 'true',
            }

            created_user = requests.post(api_user_create_url, user_data)
            result_user = json.loads(created_user.content)

            # Create profile
            # with tempfile.NamedTemporaryFile(suffix='.jpg', delete=True) as temp_image:
            #     try:
            #         resp = requests.get(user.get_picture(), stream=True).raw
            #         print(user.get_picture())
            #
            #     except requests.exceptions.RequestException as e:
            #         print('Algo salio mal')
            #
            #     try:
            #         im = Image.open(resp)
            #
            #     except IOError:
            #         print("Unable to open image")
            #
            #     # temp_image.write(im.save('sid.jpg', 'jpeg'))
            #     im.save('sid.jpg', 'jpeg')

            is_available = random.choice(['true', 'false'])

            profile_data = {
                "user": result_user.get('id'),
                "phone": user.get_phone(),
                "address": user.get_street(),
                "city": user.get_city(),
                "state": user.get_nat(),
                "zipcode": user.get_zipcode(),
                "available": 'true',
            }

            created_profile = requests.post(api_profile_create_url, profile_data)

    except Exception as error:
        print(error)


def assign_friendship():
    """
    This function assign friendship
    :return: None
    """
    api_get_users_url = API_URL + '/api/user/'
    api_url_friendsip = API_URL + '/api/friend/'

    response = requests.get(api_get_users_url)
    users = json.loads(response.content)
    users_amount = len(users)

    for user in users:
        friends_amount = random.randrange(0, users_amount-1)

        for i in range(1, friends_amount):
            friend = random.choice(users)

            while user['id'] == friend['id']:
                friend = random.choice(users)

            data = {
                "user": user['id'],
                "is_friend_of": friend['id']
            }

            friendships = requests.post(api_url_friendsip, data)

    print(friendships)


print('User amount')
amount = input()
create_users(int(amount))
# assign_friendship()
