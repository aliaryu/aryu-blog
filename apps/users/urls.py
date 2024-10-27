from django.urls import path
from .api.views import (
    UserListView,
    UserFollowersView,
    UserFollowingsView,
    UserDetailView,
    FollowUnfollowView,
    RemoveFollowerView,
)


app_name = "users"
urlpatterns = [

    # user list/detail urls
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),

    # followers/followings url
    path("<int:pk>/followers/", UserFollowersView.as_view(), name="user-followers"),
    path("<int:pk>/followings/", UserFollowingsView.as_view(), name="user-followings"),

    # follow/unfollow url
    path("<int:pk>/follow-unfollow/", FollowUnfollowView.as_view(), name="follow-unfollow"),

    # remove follower url
    path("<int:pk>/remove-follower/", RemoveFollowerView.as_view(), name="remove-follower"),
]
