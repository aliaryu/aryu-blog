from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(
            is_deleted = True,
            deleted_at = timezone.now(),
        )

    delete.queryset_only = True

    def restore(self):
        return self.update(
            is_deleted = False,
            deleted_at = None,
        )

    restore.queryset_only = True

    def hard_delete(self):
        raise NotImplementedError
        # return super().delete()

    hard_delete.queryset_only = True


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def archive(self):
        return super().get_queryset()

    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteModel:
    is_deleted = models.BooleanField(
        verbose_name = _("is deleted"),
        null = False,
        blank = True,
        default = False,
    )

    deleted_at = models.DateTimeField(
        verbose_name = _("deleted at"),
        null = True,
        blank = True
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_delete = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        raise NotImplementedError
        # super().delete()


class TimeStampModel(models.Model):
    create_at = models.DateTimeField(
        verbose_name = _("create at"),
        auto_now_add = True,
    )

    update_at = models.DateTimeField(
        verbose_name = _("update at"),
        auto_now = True,
    )

    class Meta:
        abstract = True


class BaseModel(SoftDeleteModel, TimeStampModel):
    class Meta:
        abstract = True

    objects = SoftDeleteManager()
