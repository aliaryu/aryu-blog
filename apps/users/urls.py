from django.urls import path
from .api.views import (
    UserListView,
    UserFollowersView
)



urlpatterns = [
    path("user/", UserListView.as_view(), name="user-list"),

    path("user/<int:pk>/followers/", UserFollowersView.as_view(), name="user-followers"),
    
]
