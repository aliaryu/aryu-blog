from rest_framework import generics
from .serializers import (
    UserSerializer,
    UserFollowSerializer,
)
from ..models import User
from django.db.models import Count


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().select_related("profile").annotate(
            followers_count = Count("followers", distinct=True),
            followings_count = Count("followings", distinct=True)
        )


class UserFollowersView(generics.ListAPIView):
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        return User.objects.all().filter(followings__following=self.kwargs["pk"])
