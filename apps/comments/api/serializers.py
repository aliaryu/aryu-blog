from rest_framework import serializers
from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name="users:user-detail", read_only=True, source="user")

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "answer", "create_at"]
