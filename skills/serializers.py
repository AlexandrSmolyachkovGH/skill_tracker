from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ModelSerializer,
)

from skills.models import (
    Skill,
    SkillCategory,
)
from users.models import (
    UserSkill,
)


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        read_only_fields = [
            "id",
            "name",
            "category",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class SkillWriteSerializer(ModelSerializer):
    class Meta:
        model = Skill
        exclude = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class UserSkillSerializer(ModelSerializer):
    class Meta:
        model = UserSkill
        fields = "__all__"
        read_only_fields = [
            "user",
            "skill",
        ]


class UserSkillCreateSerializer(ModelSerializer):
    name = CharField(
        max_length=100,
        min_length=3,
        required=True,
        write_only=True,
    )
    category = ChoiceField(
        choices=SkillCategory,
        default=SkillCategory.UNSPECIFIED,
        required=False,
        write_only=True,
    )

    class Meta:
        model = UserSkill
        fields = "__all__"
        read_only_fields = [
            "user",
            "skill",
        ]


class UserSkillWriteSerializer(ModelSerializer):
    name = CharField(
        max_length=100,
        min_length=3,
        required=False,
        write_only=True,
    )
    category = ChoiceField(
        choices=SkillCategory,
        required=False,
        write_only=True,
    )
    level = IntegerField(
        min_value=1,
        max_value=10,
        required=False,
    )
    xp = IntegerField(
        min_value=0,
        required=False,
    )

    class Meta:
        model = UserSkill
        fields = "__all__"
        read_only_fields = [
            "user",
            "skill",
        ]
