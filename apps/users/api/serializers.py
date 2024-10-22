from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    User,
    Profile,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["biography", "gender", "birth_date", "phone_number", "image", "profile_view"]
        read_only_fields = ["profile_view"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "id", "email", "first_name", "last_name",]


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

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True)
            if profile_serializer.is_valid(raise_exception=True):
                profile_serializer.save()
        return instance


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
