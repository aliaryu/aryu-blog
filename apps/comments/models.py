from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import BaseModel


class Comment(BaseModel):
    user = models.ForeignKey(
        verbose_name = _("user"),
        to = "users.User",
        on_delete = models.DO_NOTHING,
    )

    text = models.TextField(
        verbose_name = _("text"),
    )

    approve = models.BooleanField(
        verbose_name = _("approve"),
        default = False,
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return f"{self.user.email} - {self.text[:10]}..."
