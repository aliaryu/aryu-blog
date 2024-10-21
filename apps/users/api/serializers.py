from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    User,
    Profile,
    Follow,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["biography", "gender", "birth_date", "phone_number", "image", "profile_view"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name",]





class UserFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email"]
