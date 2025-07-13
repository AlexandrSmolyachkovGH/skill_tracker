from rest_framework.serializers import (
    ChoiceField,
    ModelSerializer,
    UUIDField,
)

from projects.models import (
    Project,
)
from users.models import UserProjectRole


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectWriteSerializer(ModelSerializer):
    class Meta:
        model = Project
        exclude = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class ProjectCreateSerializer(ModelSerializer):
    class Meta:
        model = Project
        exclude = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class AddToProjectSerializer(ModelSerializer):
    user_id = UUIDField()
    role = ChoiceField(
        choices=UserProjectRole.choices,
        default=UserProjectRole.OBSERVER,
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "user_id",
            "role",
        ]
