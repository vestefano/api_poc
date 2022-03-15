"""Accounts urls"""
from django.urls import path

from accounts import views

urlpatterns = [
    path('user/', views.ListUserApiView.as_view(), name='account_list'),
    path('user/create/', views.CreateUserApiView.as_view(), name='account_create'),
    path('user/update/<int:pk>/', views.UpdateUserApiView.as_view(), name='account_update'),
    path('user/retrieve_update/<int:pk>/', views.RetrieveUpdateUserApiView.as_view(), name='account_retrieve_update'),
    # path('user/delete/<int:pk>/', DestroyUserApiView.as_view(), name='account_destroy'),

    path('profile/', views.ListProfileApiView.as_view(), name='profile_list'),
    path('profile/<int:user_id>/', views.RetrieveProfileApiView.as_view(), name='profile_details'),
    path('profile/create/', views.CreateProfileApiView.as_view(), name='profile_create'),
    path('profile/update/<int:pk>/', views.UpdateProfileApiView.as_view(), name='profile_update'),
    path('profile/retrieve_update/<int:pk>/', views.RetrieveUpdateProfileApiView.as_view(),
         name='profile_retrieve_update'),
    # path('profile/shorter_connection/<int:pk>/<int:pk_friend>/', , name=''),

    path('friends/', views.ListCreateFriendApiView.as_view(), name='friend_list_create'),
    path('shorter_connection/<int:uid>/<int:ouid>/', views.shorter_connection_friends,
         name='shorter_connection_friends'),
]
