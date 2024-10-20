from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", ]
