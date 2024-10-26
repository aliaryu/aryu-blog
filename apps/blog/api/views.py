from rest_framework import generics
from rest_framework import views
from ..models import (
    Tag,
    Post,
)
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
)
from django.db.models import Count
from apps.comments.api.serializers import CommentSerializer
from apps.comments.models import Comment
from django.db.models import Subquery
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        ).prefetch_related("tags")


class PostCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = Post.objects.filter(slug=self.kwargs["slug"]).values("id")[:1]
        return Comment.objects.filter(
            content_type__model = "post",
            object_id = Subquery(post_id)
        )

    def perform_create(self, serializer):
        post = Post.objects.get(slug=self.kwargs["slug"])
        if not post.allow_comments:
            raise PermissionDenied(_("Comments are not allowed on this post"))
        serializer.save(
            user = self.request.user,
            content_object = post
        )
