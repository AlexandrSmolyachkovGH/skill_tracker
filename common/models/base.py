from typing import Type

from django.db import models


class TaskManager(models.Manager):
    pass


class TimeStampedModel(models.Model):
    objects: Type[TaskManager] = TaskManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
