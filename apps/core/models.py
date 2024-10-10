from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_delete=True)

    delete.queryset_only = True

    def hard_delete(self):
        return super().delete()

    hard_delete.queryset_only = True

    def restore(self):
        return self.update(is_delete=False)

    restore.queryset_only = True
    
