"""Seeder script for fill the DB"""
import json
import random

import requests
from randomuser import RandomUser


def get_request_credentials(api_url, username, password):
    """Add the JWT to header for request"""
    api_jwt_token = api_url + '/api/jwt/token/'

    data = {
        "username": username,
        "password": password,
    }

    response = requests.post(api_jwt_token, data)
    response_content = json.loads(response.content)
    token = response_content['access']

    return {'Authorization': f'Bearer {token}'}


def assign_friendship(api_url, friends_number, user_list):
    """
    This function assign friendship
    :return: None
    """
    if friends_number == 0 or not user_list:
        return

    api_url_friendship = api_url + '/api/friends/'

    min_val = min(friends_number, len(user_list) - 1)

    friends_number = friends_number - 1 if friends_number == len(user_list) else min_val

    for user in user_list:

        # Authentication
        http_auth = get_request_credentials(api_url, user['username'], user['password'])

        friends = user_list.copy()
        friends.remove(user)

        i = 0
        while i < friends_number:
            i += 1
            friend = random.choice(friends)

            data = {
                "user": str(user['id']),
                "is_friend_of": str(friend['id']),
            }

            requests.post(api_url_friendship, data, headers=http_auth)

            friends.remove(friend)


def create_users(api_url, profiles_amount, friends_number):
    """
    This function creates users with their profiles and sends them to the API.
    :param profiles_amount: Number of profiles you want to generate
    :return: None
    """
    if profiles_amount == 0:
        return

    profiles = RandomUser.generate_users(profiles_amount)
    api_user_create_url = api_url + '/api/user/create/'
    api_profile_create_url = api_url + '/api/profile/create/'
    user_list = []

    for profile in profiles:
        # Create User
        user_data = {
            "username": profile.get_username(),
            "first_name": profile.get_first_name(),
            "last_name": profile.get_last_name(),
            "email": profile.get_email(),
            "password": profile.get_password(),
        }

        response = requests.post(api_user_create_url, user_data)

        user = json.loads(response.content)

        user_list.append({
            "id": user['id'],
            "username": profile.get_username(),
            "password": profile.get_password(),
        })

        # Authentication
        http_auth = get_request_credentials(api_url, profile.get_username(), profile.get_password())

        # Create profile
        profile_data = {
            "phone": profile.get_phone(),
            "address": profile.get_street(),
            "city": profile.get_city(),
            "state": profile.get_nat(),
            "zipcode": profile.get_zipcode(),
            "img": profile.get_picture(),
            "available": 'true',
        }

        requests.post(api_profile_create_url, profile_data, headers=http_auth)

    assign_friendship(api_url, friends_number, user_list)

    for user in user_list:
        print(user)


if __name__ == '__main__':

    print('Api url like # http://localhost:8000')
    api_host = input()

    print('Profile amount')
    profile_amount = input()

    print('Friends amount')
    friendships = input()

    if not api_host:
        api_host = 'http://localhost:8000'

    create_users(api_host, int(profile_amount), int(friendships))
