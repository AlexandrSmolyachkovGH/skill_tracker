import uuid

from django.core.validators import MinLengthValidator
from django.db import models

from common.models.base import TimeStampedModel


class ProjectStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    ACTIVE = 'active', 'Активный'
    PAUSED = 'paused', 'Приостановлен'
    COMPLETED = 'completed', 'Завершён'
    CANCELED = 'canceled', 'Отменён'


class Project(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ],
    )
    status = models.CharField(
        choices=ProjectStatus.choices,
        default=ProjectStatus.DRAFT,
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = [
            'created_at',
        ]

    def __str__(self) -> str:
        return f"Project: {self.name}, status: {self.status}"
