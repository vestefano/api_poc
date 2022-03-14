"""Accounts urls"""
from django.urls import path

from accounts.views import ListProfileApiView, CreateProfileApiView, RetrieveProfileApiView, UpdateProfileApiView, \
     RetrieveUpdateProfileApiView

urlpatterns = [
    path('profile/', ListProfileApiView.as_view(), name='profile_list'),
    path('profile/<int:user_id>/', RetrieveProfileApiView.as_view(), name='profile_details'),
    path('profile/create/', CreateProfileApiView.as_view(), name='profile_create'),
    path('profile/update/<int:pk>/', UpdateProfileApiView.as_view(), name='profile_update'),
    path('profile/retrieve_update/<int:pk>/', RetrieveUpdateProfileApiView.as_view(), name='profile__retrieve_update'),
    # path('profile/shorter_connection/<int:pk>/<int:pk_friend>/', , name=''),
]
