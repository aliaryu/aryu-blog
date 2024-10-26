from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    Tag,
    Post,
)
from apps.comments.api.serializers import CommentSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag_name"]


class PostListSerializer(serializers.ModelSerializer):
    author_detail = serializers.HyperlinkedRelatedField(view_name="users:user-detail", read_only=True, source="author")
    author_email = serializers.EmailField(source="author.email", read_only=True)
    content = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail", lookup_field="slug")

    class Meta:
        model = Post
        fields = [
            "url", "id" , "author_detail", "author_email", "title", "content",
            "post_view", "likes_count",
        ]

    def get_content(self, obj):
        return obj.content[:17] + "..."


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author_detail = serializers.HyperlinkedRelatedField(view_name="users:user-detail", read_only=True, source="author")
    author_email = serializers.EmailField(source="author.email", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments = serializers.HyperlinkedIdentityField(view_name="blog:post-comments", lookup_field="slug")
    
    class Meta:
        model = Post
        fields = [
            "id" , "author_detail", "author_email", "title", "content", "create_at", "update_at",
            "allow_comments", "post_view", "likes_count", "tags", "comments"
        ]
        read_only_fields = ["create_at", "update_at", "post_view"]
