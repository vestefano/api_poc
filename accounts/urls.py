"""Accounts urls"""
from django.urls import path

from accounts.views import ListProfileApiView, CreateProfileApiView, RetrieveProfileApiView, UpdateProfileApiView, \
    RetrieveUpdateProfileApiView, ListUserApiView, CreateUserApiView, UpdateUserApiView, RetrieveUpdateUserApiView, \
    ListCreateFriendApiView

urlpatterns = [
    path('user/', ListUserApiView.as_view(), name='account_list'),
    path('user/create/', CreateUserApiView.as_view(), name='account_create'),
    path('user/update/<int:pk>/', UpdateUserApiView.as_view(), name='account_update'),
    path('user/retrieve_update/<int:pk>/', RetrieveUpdateUserApiView.as_view(), name='account_retrieve_update'),
    # path('user/delete/<int:pk>/', DestroyUserApiView.as_view(), name='account_destroy'),
    path('profile/', ListProfileApiView.as_view(), name='profile_list'),
    path('profile/<int:user_id>/', RetrieveProfileApiView.as_view(), name='profile_details'),
    path('profile/create/', CreateProfileApiView.as_view(), name='profile_create'),
    path('profile/update/<int:pk>/', UpdateProfileApiView.as_view(), name='profile_update'),
    path('profile/retrieve_update/<int:pk>/', RetrieveUpdateProfileApiView.as_view(), name='profile_retrieve_update'),
    # path('profile/shorter_connection/<int:pk>/<int:pk_friend>/', , name=''),
    path('friend/', ListCreateFriendApiView.as_view(), name='friend_list_create')
]
