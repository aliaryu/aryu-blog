from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    User,
    Profile,
)
from django.contrib.auth.password_validation import validate_password as v_password


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["biography", "gender", "birth_date", "phone_number", "image", "profile_view"]
        read_only_fields = ["profile_view"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "id", "email", "first_name", "last_name",]
        extra_kwargs = {
            "url": {"view_name": "users:user-detail"},
        }


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    # this fields need annotate in related view
    followers_count = serializers.IntegerField(read_only=True)
    followings_count = serializers.IntegerField(read_only=True)

    followers_url = serializers.HyperlinkedIdentityField(view_name="users:user-followers", lookup_field="pk")
    followings_url = serializers.HyperlinkedIdentityField(view_name="users:user-followings", lookup_field="pk")

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
        fields = ["url", "id", "email"]
        extra_kwargs = {
            "url": {"view_name": "users:user-detail"},
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(_("passwords do not match"))
        return data
    
    def validate_password(self, value):
        v_password(value)
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")  
        user = User.objects.create_user(**validated_data)
        return user
