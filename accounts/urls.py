"""Accounts urls"""
from django.urls import path

from accounts import views

urlpatterns = [
    path('user/create/', views.CreateUserApiView.as_view(), name='account_create'),
    path('user/<int:pk>/', views.RetrieveUpdateDeleteUserApiView.as_view(), name='account_retrieve_update_delete'),

    path('manager/', views.AdminListCreateUserApiView.as_view(), name='account_manager_list_create'),
    path('manager/<int:pk>/', views.AdminRetrieveUpdateDeleteUserApiView.as_view(),
         name='account_manager_retrieve_update_delete'),

    path('profile/', views.ListProfileApiView.as_view(), name='profile_list'),
    path('profile/create/', views.CreateProfileApiView.as_view(), name='profile_create'),
    path('profile/<int:user_id>/', views.RetrieveProfileApiView.as_view(), name='profile_details'),
    path('profile/update/<int:user_id>/', views.UpdateProfileApiView.as_view(), name='profile_update'),
    path('profile/delete/<int:user_id>/', views.DestroyProfileApiView.as_view(), name='profile_delete'),

    path('friends/', views.ListCreateFriendApiView.as_view(), name='friend_list_create'),
    path('friends/<int:user_id>/', views.RetrieveFriendsApiView.as_view(), name='friends_profiles'),
    path('friends/delete/<int:user_id>/<int:friend_id>/', views.DeleteFriendshipAPIView.as_view(),
         name='friendship_delete'),
    path('shorter_connection/<int:uid>/<int:ouid>/', views.ShorterConnectionFriends.as_view(),
         name='shorter_connection_friends'),
]
