import uuid

from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

from common.models.base import TimeStampedModel


class UserProjectRole(models.TextChoices):
    CREATOR = 'creator', 'Владелец'
    PARTICIPANT = 'participant', 'Участник'
    MENTOR = 'mentor', 'Наставник'
    OBSERVER = 'observer', 'Наблюдатель'


class User(TimeStampedModel):
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
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )

    class Meta:
        ordering = [
            'created_at',
        ]

    def __str__(self) -> str:
        return f"User: {self.name}, email: {self.email}"


class UserSkill(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.SET_NULL,
        null=True,
    )
    level = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    xp = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
    )

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self) -> str:
        return (
            f"user: {self.user}, skill: {self.skill},"
            f"level: {self.level}, xp: {self.xp}"
        )


class UserProject(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
    )
    role = models.CharField(
        choices=UserProjectRole.choices,
        default=UserProjectRole.CREATOR,
    )

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self) -> str:
        return f"user: {self.user}, project: {self.project}, role: {self.role}"
