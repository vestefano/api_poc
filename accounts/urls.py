"""Accounts urls"""
from django.urls import path

from accounts import views

urlpatterns = [
    path('user/create/', views.CreateUserApiView.as_view(), name='account_create'),
    path('user/<int:pk>/', views.RetrieveUserApiView.as_view(), name='account_details'),
    path('user/update/<int:pk>/', views.UpdateUserApiView.as_view(), name='account_update'),
    path('user/delete/<int:pk>/', views.DestroyUserApiView.as_view(), name='account_delete'),

    path('manager/', views.AdminListUserApiView.as_view(), name='account_manager_list'),
    path('manager/', views.AdminCreateUserApiView.as_view(), name='account_manager_create'),
    path('manager/<int:pk>/', views.AdminRetrieveUserApiView.as_view(), name='account_manager_details'),
    path('manager/update/<int:pk>/', views.AdminUpdateUserApiView.as_view(), name='account_manager_update'),
    path('manager/delete/<int:pk>/', views.AdminDestroyUserApiView.as_view(), name='account_manager_delete'),

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
