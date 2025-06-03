import uuid

from django.core.validators import MinLengthValidator
from django.db import models

from common.models.base import TimeStampedModel


class SkillCategory(models.TextChoices):
    UNSPECIFIED = 'unspecified', 'Неопределенный'
    PROGRAMMING = 'programming', 'Программирование'
    DESIGN = 'design', 'Дизайн'
    MARKETING = 'marketing', 'Маркетинг'
    MANAGEMENT = 'management', 'Менеджмент'
    WRITING = 'writing', 'Копирайтинг'
    OTHER = 'other', 'Другое'


class Skill(TimeStampedModel):
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
    category = models.CharField(
        choices=SkillCategory.choices,
        default=SkillCategory.UNSPECIFIED,
    )

    class Meta:
        ordering = [
            'created_at',
        ]

    def __str__(self) -> str:
        return f"Skill: {self.name}, category: {self.category}"
