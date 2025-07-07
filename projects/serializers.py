from rest_framework.serializers import ModelSerializer

from projects.models import (
    Project,
)


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
