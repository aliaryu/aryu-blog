from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from django.utils.text import slugify
from time import time
from django.contrib.contenttypes.fields import GenericRelation


class Tag(BaseModel):
    tag_name = models.CharField(
        verbose_name = _("tag"),
        max_length = 255,
        unique = True,
    )

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return f"{self.tag_name}"


class Post(BaseModel):
    author = models.ForeignKey(
        verbose_name = _("author"),
        to = "users.User",
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

    comments = GenericRelation(
        to = "comments.Comment",
        # related_query_name = "post_comments",
    )

    def save(self, *args, **kwargs):
        if not self.id:
            slugify_title = slugify(self.title, allow_unicode=True)
            time_stamp = int(time())
            self.slug = f"{slugify_title}-{time_stamp}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return f"{self.title}"
