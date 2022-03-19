# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['AdminUserApiViewsTest::test_list_users 1'] = [
    {
        'email': 'jhon@example.com',
        'first_name': 'Jhon',
        'id': 1,
        'is_active': True,
        'is_superuser': True,
        'last_name': 'Doe',
        'username': 'JD2022'
    },
    {
        'email': 'martha@example.com',
        'first_name': 'Martha',
        'id': 2,
        'is_active': True,
        'is_superuser': False,
        'last_name': 'Doe',
        'username': 'Martha96'
    },
    {
        'email': 'mikael@example.com',
        'first_name': 'Mikael',
        'id': 3,
        'is_active': True,
        'is_superuser': True,
        'last_name': 'Sans',
        'username': 'Mikael564'
    }
]

snapshots['FriendsApiViewsTest::test_user_friends_profiles_list 1'] = {
    'friends': [
        {
            'address': '3494 Sunset St',
            'available': True,
            'city': 'Italy',
            'first_name': 'Ana',
            'friends': [
                5
            ],
            'img': 'https://randomuser.me/api/portraits/women/65.jpg',
            'last_name': 'Sans',
            'phone': '(390)-568-1958',
            'state': 'IT',
            'user_id': 2,
            'zipcode': '65487'
        },
        {
            'address': '4738 Fairview St',
            'available': True,
            'city': 'Poland',
            'first_name': 'Juan',
            'friends': [
                4
            ],
            'img': 'https://randomuser.me/api/portraits/women/65.jpg',
            'last_name': 'Sans',
            'phone': '(396)-158-3397',
            'state': 'PL',
            'user_id': 3,
            'zipcode': '65487'
        }
    ]
}

snapshots['ProfilesApiViewsTest::test_list_profile 1'] = [
    {
        'address': '8655 Frances Ct',
        'available': True,
        'city': 'Paris',
        'first_name': 'Jhon',
        'friends': [
            2,
            3
        ],
        'img': 'https://randomuser.me/api/portraits/women/65.jpg',
        'last_name': 'Doe',
        'phone': '(925)-967-1402',
        'state': 'FR',
        'user_id': 1,
        'zipcode': '65487'
    },
    {
        'address': '1401 Oak Lawn Ave',
        'available': False,
        'city': 'Canada',
        'first_name': 'Martha',
        'friends': [
            3
        ],
        'img': 'https://randomuser.me/api/portraits/women/56.jpg',
        'last_name': 'Doe',
        'phone': '(463)-159-7835',
        'state': 'CD',
        'user_id': 2,
        'zipcode': '98752'
    },
    {
        'address': '8909 Walnut Hill Ln',
        'available': True,
        'city': 'Mexico',
        'first_name': 'Mikael',
        'friends': [
            1
        ],
        'img': 'https://randomuser.me/api/portraits/women/56.jpg',
        'last_name': 'Sans',
        'phone': '(709)-501-3504',
        'state': 'MX',
        'user_id': 3,
        'zipcode': '85245'
    }
]

snapshots['UserApiViewsTest::test_owner_retrieve_account 1'] = {
    'email': 'jhon@example.com',
    'first_name': 'Jhon',
    'id': 1,
    'last_name': 'Doe',
    'username': 'JD2022'
}
