from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    UUIDField,
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
    name = CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
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
    user_id = UUIDField()
    project_id = UUIDField()

    class Meta:
        model = UserProject
        fields = [
            "user_id",
            "project_id",
            "role",
        ]


class ListUsersProjectSerializer(ModelSerializer):
    user_id = UUIDField(
        source="user.id",
        read_only=True,
    )

    class Meta:
        model = UserProject
        fields = [
            "user_id",
        ]


class UserRoleSerializer(ModelSerializer):
    class Meta:
        model = UserProject
        fields = ["user_id", "role"]
