from rest_framework.serializers import ModelSerializer

from users.models import (
    User,
    UserProject,
    UserSkill,
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSkillSerializer(ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'


class UserProjectSerializer(ModelSerializer):
    class Meta:
        model = UserProject
        fields = '__all__'
