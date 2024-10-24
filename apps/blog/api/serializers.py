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


class PostSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True)
    author_detail = serializers.HyperlinkedRelatedField(view_name="users:user-detail", read_only=True, source="author")
    author_email = serializers.EmailField(source="author.email", read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id" , "author_detail", "author_email", "title", "content", "post_view",
            "tags",
        ]

    def get_content(self, obj):
        return obj.content[:17] + "..."
