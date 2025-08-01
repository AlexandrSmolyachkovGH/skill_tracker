from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    UUIDField,
)

from projects.models import (
    Project,
    ProjectStatus,
)
from users.models import (
    User,
    UserProject,
)
from users.serializers import UserRoleSerializer, UserSerializer


class ProjectSerializer(ModelSerializer):
    owner = UserSerializer(
        read_only=True,
    )
    project_users_role = UserRoleSerializer(
        read_only=True,
        source="project_users",
        many=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "status",
            "owner",
            "project_users_role",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "name",
            "status",
            "owner",
            "project_users_role",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class ProjectWriteSerializer(ModelSerializer):
    owner = UserSerializer(
        read_only=True,
    )
    name = CharField(
        required=False,
    )
    status = ChoiceField(
        choices=ProjectStatus.choices,
        required=False,
    )
    project_users_role = UserRoleSerializer(
        read_only=True,
        source="project_users",
        many=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "project_users_role",
            "name",
            "status",
            "owner",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "project_users_role",
            "owner",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class ProjectCreateSerializer(ModelSerializer):
    owner = UserSerializer(
        read_only=True,
    )
    project_users_role = UserRoleSerializer(
        read_only=True,
        source="project_users",
        many=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "project_users_role",
            "name",
            "status",
            "owner",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "project_users_role",
            "owner",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class AddToProjectSerializer(ModelSerializer):
    user = UserSerializer(
        read_only=True,
    )
    user_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
    )
    project = ProjectSerializer(
        read_only=True,
    )
    project_id = UUIDField(
        source="project.id",
        read_only=True,
    )

    class Meta:
        model = UserProject
        fields = [
            "id",
            "project_id",
            "project",
            "user_id",
            "user",
            "role",
        ]
        read_only_fields = [
            "id",
            "project_id",
            "project",
            "user",
        ]
