from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
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
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from apps.core.permissions import (
    IsUserOwnerOrReadOnly,
    ReadOnly,
)
from rest_framework.filters import SearchFilter
from apps.core.paginations import SmallResultPagination


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated|ReadOnly]
    pagination_class = SmallResultPagination
    filter_backends = [SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        return Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    permission_classes = [IsUserOwnerOrReadOnly|IsAdminUser]

    def get_queryset(self):
        return Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        ).prefetch_related("tags")


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