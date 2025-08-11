from rest_framework.serializers import (
    CharField,
    ChoiceField,
    ModelSerializer,
)

from projects.serializers import ProjectSerializer
from tasks.models import (
    Task,
    TaskAttachment,
    TaskStatus,
)


class TaskSerializer(ModelSerializer):
    owner_name = CharField(
        source="assigned_to.name",
        read_only=True,
    )
    project_data = ProjectSerializer(
        source="project",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "assigned_to",
            "owner_name",
            "project_data",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class TaskCreateSerializer(ModelSerializer):
    user_name = CharField(
        source="assigned_to.name",
        read_only=True,
    )
    project_name = CharField(
        source="project.name",
        read_only=True,
    )
    status = ChoiceField(
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "user_name",
            "assigned_to",
            "project_name",
            "project",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "user_name",
            "assigned_to",
            "project_name",
            "project",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class TaskPartialUpdateSerializer(ModelSerializer):
    user_name = CharField(
        source="assigned_to.name",
        read_only=True,
    )
    project_name = CharField(
        source="project.name",
        read_only=True,
    )
    status = ChoiceField(
        choices=TaskStatus.choices,
        required=False,
    )
    title = CharField(
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "user_name",
            "assigned_to",
            "project_name",
            "project",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "user_name",
            "assigned_to",
            "project_name",
            "project",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class TaskAttachmentSerializer(ModelSerializer):
    task_name = CharField(
        source="task.title",
        read_only=True,
    )

    class Meta:
        model = TaskAttachment
        fields = [
            "id",
            "task",
            "task_name",
            "file_url",
        ]


class TaskAttachmentWriteSerializer(ModelSerializer):
    task_name = CharField(
        source="task.title",
        read_only=True,
    )
    file_url = CharField(
        required=True,
    )

    class Meta:
        model = TaskAttachment
        fields = [
            "id",
            "task",
            "task_name",
            "file_url",
        ]
        read_only_fields = [
            "id",
            "task",
            "task_name",
        ]


class TaskAttachmentCreateSerializer(ModelSerializer):
    task_name = CharField(
        source="task.title",
        read_only=True,
    )
    file_url = CharField(
        default="waiting for loading",
    )

    class Meta:
        model = TaskAttachment
        fields = [
            "id",
            "task",
            "task_name",
            "file_url",
        ]
        read_only_fields = [
            "id",
            "task",
            "task_name",
        ]
