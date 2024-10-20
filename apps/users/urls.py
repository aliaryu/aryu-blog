from django.urls import path
from .api.views import (
    UserListView
)



urlpatterns = [
    path("user/", UserListView.as_view(), name="user-list")
    
]
