from django.db import models

from .cashing_queryset import CachingQuerySet


class CachingManager(models.Manager):
    def get_queryset(self):
        return CachingQuerySet(self.model, using=self._db)