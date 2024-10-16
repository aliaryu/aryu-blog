from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Post(BaseModel):
    author = models.ForeignKey(
        verbose_name = _("author"),
        to = "User",
        on_delete = models.DO_NOTHING,
        related_name = "posts",
    )

    title = models.CharField(
        verbose_name = _("title"),
        max_length = 100,
        blank = False,
        null = False,
    )

    slug = models.SlugField(
        verbose_name = _("slug"),
        max_length = 150,
        blank = True,
        null = False,
        unique = True,
    )

    content = models.TextField(
        verbose_name = _("content"),
        blank = False,
        null = False,
    )

    post_view = models.PositiveIntegerField(
        verbose_name = _("post view"),
        default = 1,
    )

    allow_comments = models.BooleanField(
        verbose_name = _("allow comments"),
        blank = True,
        null = False,
        default = True,
    )

    tags = models.ManyToManyField(
        verbose_name = _("tags"),
        to = "Tag",
        related_name = "posts",
    )

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return f"{self.title}"
