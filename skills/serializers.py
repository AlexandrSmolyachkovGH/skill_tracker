from rest_framework.serializers import ModelSerializer

from skills.models import (
    Skill,
)


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class SkillWriteSerializer(ModelSerializer):
    class Meta:
        model = Skill
        exclude = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
