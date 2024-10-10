from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_delete=True)

    delete.queryset_only = True

    def hard_delete(self):
        raise NotImplementedError
        # return super().delete()

    hard_delete.queryset_only = True

    def restore(self):
        return self.update(is_delete=False)

    restore.queryset_only = True


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)

    def archive(self):
        return super().get_queryset()

    def deleted(self):
        return super().get_queryset().filter(is_delete=True)

