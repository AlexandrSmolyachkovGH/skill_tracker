from rest_framework.serializers import ModelSerializer

from tasks.models import (
    Task,
    TaskAttachment,
)


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskAttachmentSerializer(ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = '__all__'
