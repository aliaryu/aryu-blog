from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    User,
    Profile,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "biography", "gender", "birth_date", "phone_number", "image", "profile_view"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile"]
