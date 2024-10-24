from rest_framework import generics
from rest_framework import views
from ..models import (
    Tag,
    Post,
)
from .serializers import (
    PostSerializer,
)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()
