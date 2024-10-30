from django.urls import path
from .api.views import (
    PostListView,
    PostDetailView,
    PostCommentsView,
    PostLikeUnlikeView
)


app_name = "blog"
urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),

    # post comments url
    path("posts/<slug:slug>/comments/", PostCommentsView.as_view(), name="post-comments"),

    # like/unlike post url
    path("posts/<slug:slug>/like-unlike/", PostLikeUnlikeView.as_view(), name="post-like-unlike")

]
