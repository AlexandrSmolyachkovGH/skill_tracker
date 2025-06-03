import uuid

from django.core.validators import MinLengthValidator
from django.db import models

from common.models.base import TimeStampedModel


class TaskStatus(models.TextChoices):
    NEW = 'new', 'Новая'
    IN_PROGRESS = 'in_progress', 'В работе'
    COMPLETED = 'completed', 'Завершена'
    CANCELED = 'canceled', 'Отменена'


class Task(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ],
    )
    status = models.CharField(
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
    )
    assigned_to = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = [
            'created_at',
        ]

    def __str__(self) -> str:
        return f"Task: {self.title}, status: {self.status}"


class TaskAttachment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
    )
    file_id = models.UUIDField(
        blank=True,
        null=True,
        help_text="UUID файла в файловом сервисе",
    )

    def __str__(self) -> str:
        file = self.file_id if self.file_id else "No data"
        return f"TaskID: {self.task}, FileID: {file}"
