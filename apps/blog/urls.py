from django.urls import path
from .api.views import (
    PostListView,
    PostDetailView,
    PostCommentsView
)


app_name = "blog"
urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),

    # post comments
    path("posts/<slug:slug>/comments/", PostCommentsView.as_view(), name="post-comments"),

]
