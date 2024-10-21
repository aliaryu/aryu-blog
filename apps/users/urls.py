from django.urls import path
from .api.views import (
    UserListView,
    UserFollowersView,
    UserFollowingsView,
    UserDetailView,
)



urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    # followers/followings urls
    path("<int:pk>/followers/", UserFollowersView.as_view(), name="user-followers"),
    path("<int:pk>/followings/", UserFollowingsView.as_view(), name="user-followings"),
    
]
