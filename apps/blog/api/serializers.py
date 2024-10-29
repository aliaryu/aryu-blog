from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import (
    Tag,
    Post,
)


class TagSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField()

    class Meta:
        model = Tag
        fields = ["id", "tag_name"]


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
    tags = TagSerializer(many=True, required=False)
    author_detail = serializers.HyperlinkedRelatedField(view_name="users:user-detail", read_only=True, source="author")
    author_email = serializers.EmailField(source="author.email", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments = serializers.HyperlinkedIdentityField(view_name="blog:post-comments", lookup_field="slug")

    class Meta:
        model = Post
        fields = [
            "id" , "author_detail", "author_email", "title", "content", "create_at", "update_at",
            "allow_comments", "post_view", "likes_count", "tags", "comments",
        ]
        read_only_fields = ["create_at", "update_at", "post_view"]

    def get_or_create_tags(self, tags):
        tag_names = [tag.get("tag_name") for tag in tags]
        existing_tag_names = set(Tag.objects.filter(tag_name__in=tag_names).values_list("tag_name", flat=True))
        new_tags = [Tag(tag_name=tag_name) for tag_name in tag_names if tag_name not in existing_tag_names]
        if new_tags:
            Tag.objects.bulk_create(new_tags)
        all_tags = Tag.objects.filter(tag_name__in=tag_names)
        return all_tags

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", [])
        if tags:
            instance.tags.set(self.get_or_create_tags(tags))
        fields = ["title", "content", "allow_comments"]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:
                pass
        instance.save()
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
