from django.urls import path
from .api.views import (
    PostListView,
)


app_name = "blog"
urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
]
