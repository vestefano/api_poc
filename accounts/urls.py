"""Accounts urls"""
from django.urls import path

from accounts import views

urlpatterns = [
    path('user/', views.ListUserApiView.as_view(), name='account_list'),
    path('user/create/', views.CreateUserApiView.as_view(), name='account_create'),
    path('user/<int:pk>/', views.RetrieveUserApiView.as_view(), name='account_details'),
    path('user/update/<int:pk>/', views.UpdateUserApiView.as_view(), name='account_update'),
    path('user/delete/<int:pk>/', views.DestroyUserApiView.as_view(), name='account_delete'),

    path('profile/', views.ListProfileApiView.as_view(), name='profile_list'),
    path('profile/create/', views.CreateProfileApiView.as_view(), name='profile_create'),
    path('profile/<int:user_id>/', views.RetrieveProfileApiView.as_view(), name='profile_details'),
    path('profile/update/<int:pk>/', views.UpdateProfileApiView.as_view(), name='profile_update'),
    path('profile/delete/<int:pk>/', views.DestroyProfileApiView.as_view(), name='profile_delete'),

    path('friends/', views.ListCreateFriendApiView.as_view(), name='friend_list_create'),
    path('shorter_connection/<int:uid>/<int:ouid>/', views.ShorterConnectionFriends.as_view(),
         name='shorter_connection_friends'),
]
