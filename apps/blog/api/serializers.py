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

    author_detail = serializers.HyperlinkedRelatedField(view_name="users:user-detail", read_only=True, source="author")
    author_email = serializers.EmailField(source="author.email", read_only=True)
    content = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id" , "author_detail", "author_email", "title", "content", "post_view", "likes_count",
        ]

    def get_content(self, obj):
        return obj.content[:17] + "..."
