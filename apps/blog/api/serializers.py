from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    Tag,
    Post,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag_name"]


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author_email", "title", "content", "post_view", "tags"]
