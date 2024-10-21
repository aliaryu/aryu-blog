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


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    # this fields need annotate in related view
    followers_count = serializers.IntegerField(read_only=True)
    followings_count = serializers.IntegerField(read_only=True)

    followers_url = serializers.HyperlinkedIdentityField(view_name="user-followers", lookup_field="pk")
    followings_url = serializers.HyperlinkedIdentityField(view_name="user-followings", lookup_field="pk")

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "profile",
            "followers_count", "followings_count",
            "followers_url", "followings_url",
        ]


class UserFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email"]
