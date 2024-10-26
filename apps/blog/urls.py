from django.urls import path
from .api.views import (
    PostListView,
    PostDetailView,
)


app_name = "blog"
urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
]
