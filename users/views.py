from typing import Type

from drf_spectacular.utils import extend_schema
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
)

from users.models import (
    User,
    UserProject,
    UserSkill,
)
from users.serializers import (
    UserProjectSerializer,
    UserProjectWriteSerializer,
    UserSerializer,
    UserSkillSerializer,
    UserSkillWriteSerializer,
    UserWriteSerializer,
)

router = SimpleRouter()


@extend_schema(tags=["Users"])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return UserSerializer
        return UserWriteSerializer


@extend_schema(tags=["Users-Skills"])
class UserSkillViewSet(ModelViewSet):
    queryset = UserSkill.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return UserSkillSerializer
        return UserSkillWriteSerializer


@extend_schema(tags=["Users-Projects"])
class UserProjectViewSet(ModelViewSet):
    queryset = UserProject.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return UserProjectSerializer
        return UserProjectWriteSerializer


router.register(r"", UserViewSet, basename="users")
router.register(r"skills", UserSkillViewSet, basename="user-skills")
router.register(r"projects", UserProjectViewSet, basename="user-projects")
