from rest_framework.serializers import (
    CharField,
    ModelSerializer,
)

from tasks.models import (
    Task,
    TaskAttachment,
)


class TaskSerializer(ModelSerializer):
    user_name = CharField(
        source="assigned_to.name",
        read_only=True,
    )
    project_name = CharField(
        source="project.name",
        read_only=True,
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
        ]


class TaskWriteSerializer(ModelSerializer):
    class Meta:
        model = Task
        exclude = [
            "id",
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
    class Meta:
        model = TaskAttachment
        exclude = [
            "id",
        ]
