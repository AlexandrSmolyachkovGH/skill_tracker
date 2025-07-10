from rest_framework.serializers import (
    CharField,
    ModelSerializer,
)

from users.models import (
    User,
    UserProject,
    UserSkill,
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserWriteSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
        ]


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class UserSkillSerializer(ModelSerializer):
    user_name = CharField(
        source="user.name",
        read_only=True,
    )
    skill_name = CharField(
        source="skill.name",
        read_only=True,
    )

    class Meta:
        model = UserSkill
        fields = [
            "user",
            "user_name",
            "skill",
            "skill_name",
            "level",
            "xp",
        ]


class UserSkillWriteSerializer(ModelSerializer):
    class Meta:
        model = UserSkill
        fields = "__all__"


class UserProjectSerializer(ModelSerializer):
    user_name = CharField(
        source="user.name",
        read_only=True,
    )
    project_name = CharField(
        source="project.name",
        read_only=True,
    )

    class Meta:
        model = UserProject
        fields = [
            "user_name",
            "user",
            "project_name",
            "project",
            "role",
        ]


class UserProjectWriteSerializer(ModelSerializer):
    class Meta:
        model = UserProject
        fields = "__all__"
