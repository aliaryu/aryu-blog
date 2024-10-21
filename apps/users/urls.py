from django.urls import path
from .api.views import (
    UserListView,
    UserFollowersView,
    UserFollowingsView,
)



urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),

    # followers/followings urls
    path("user/<int:pk>/followers/", UserFollowersView.as_view(), name="user-followers"),
    path("user/<int:pk>/followings/", UserFollowingsView.as_view(), name="user-followings"),
    
]
