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


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.all().select_related("author").annotate(
            likes_count = Count("likes", distinct=True)
        )
