from rest_framework import generics
from .serializers import (
    UserSerializer
)
from ..models import User


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
