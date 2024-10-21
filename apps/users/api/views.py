from rest_framework import generics
from .serializers import (
    UserSerializer,
)
from ..models import User
from django.db.models import Count


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().annotate(
            followers_count = Count('followers', distinct=True),
            followings_count = Count('followings', distinct=True)
        )
