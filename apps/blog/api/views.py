from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from ..models import (
    Post,
)
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
)
from django.db.models import Count
from apps.comments.api.serializers import CommentSerializer
from apps.comments.models import Comment
from django.db.models import Subquery, F
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from apps.core.permissions import (
    IsUserOwnerOrReadOnly,
    ReadOnly,
)
from rest_framework.filters import SearchFilter
from apps.core.paginations import SmallResultPagination
from apps.core.utils import get_client_ip
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated|ReadOnly]
    pagination_class = SmallResultPagination
    filter_backends = [SearchFilter]
    search_fields = ["title", "tags__tag_name"]

    def get_queryset(self):
        return Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        )
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostListSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    permission_classes = [IsUserOwnerOrReadOnly|IsAdminUser]

    def get_queryset(self):
        queryset = Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        ).prefetch_related("tags")

        # post view update + cache ip to avoid increasing fake post view
        slug = self.kwargs.get("slug")
        user_ip = get_client_ip(self.request)
        cache_key = f"post_view_{slug}_{user_ip}"
        last_view_time = cache.get(cache_key)

        if not last_view_time or timezone.now() - last_view_time > timedelta(seconds=10):
            queryset.filter(slug=slug).update(post_view=F("post_view") + 1)
            cache.set(cache_key, timezone.now(), timeout=600)
        return queryset


class PostCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated|ReadOnly]
    pagination_class = SmallResultPagination

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


class PostLikeUnlikeView(views.APIView):
    queryset = Post.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Post.objects.get(slug=self.kwargs["slug"])

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        if post.likes.filter(id=user.id).exists():
            return Response({"detail": _("you have already liked this post")}, status=status.HTTP_400_BAD_REQUEST)
        post.likes.add(user)
        return Response({"detail": _("post liked successfully")}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        if not post.likes.filter(id=user.id).exists():
            return Response({"detail": _("you have not liked this post")}, status=status.HTTP_400_BAD_REQUEST)
        post.likes.remove(user)
        return Response({"detail": _("post unliked successfully")}, status=status.HTTP_204_NO_CONTENT)
