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
