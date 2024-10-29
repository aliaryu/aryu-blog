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
    tags = serializers.SerializerMethodField()
    update_tags = serializers.ListField(
        child = serializers.CharField(),
        write_only = True,
        required = False
    )
    author_detail = serializers.HyperlinkedRelatedField(view_name="users:user-detail", read_only=True, source="author")
    author_email = serializers.EmailField(source="author.email", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments = serializers.HyperlinkedIdentityField(view_name="blog:post-comments", lookup_field="slug")

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    class Meta:
        model = Post
        fields = [
            "id" , "author_detail", "author_email", "title", "content", "create_at", "update_at",
            "allow_comments", "post_view", "likes_count", "tags", "update_tags", "comments",
        ]
        read_only_fields = ["create_at", "update_at", "post_view"]

    def update(self, instance, validated_data):
        tags_list = validated_data.pop("update_tags", [])
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.allow_comments = validated_data.get("allow_comments", instance.allow_comments)
        instance.save()

        if tags_list:
            existing_tags = set(Tag.objects.filter(tag_name__in=tags_list).values_list("tag_name", flat=True))
            new_tags = [Tag(tag_name=tag_name) for tag_name in tags_list if tag_name not in existing_tags and tag_name]
            if new_tags:
                Tag.objects.bulk_create(new_tags)
            all_tags = Tag.objects.filter(tag_name__in=tags_list)
            instance.tags.set(all_tags)
        return instance


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child = serializers.CharField(), write_only=True
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags", "allow_comments"]

    def create(self, validated_data):
        tags_list = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        existing_tags = set(Tag.objects.filter(tag_name__in=tags_list).values_list("tag_name", flat=True))
        new_tags = [Tag(tag_name=tag_name) for tag_name in tags_list if tag_name not in existing_tags]
        if new_tags:
            Tag.objects.bulk_create(new_tags)
        all_tags = Tag.objects.filter(tag_name__in=tags_list)
        post.tags.set(all_tags)
        return post
