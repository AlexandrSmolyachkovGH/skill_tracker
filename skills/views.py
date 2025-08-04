from typing import (
    Any,
    Type,
)

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
)
from rest_framework_nested.routers import (
    NestedSimpleRouter,
)

from skills.serializers import (
    SkillSerializer,
    UserSkillCreateSerializer,
    UserSkillSerializer,
    UserSkillWriteSerializer,
)
from skills.services.skill_service import skill_service
from users.views import router as user_router


@extend_schema(tags=["Skills"])
class SkillViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return UserSkillSerializer
        if self.action == "create":
            return UserSkillCreateSerializer
        if self.action == "destroy":
            return SkillSerializer
        return UserSkillWriteSerializer

    def get_permissions(
        self,
    ) -> list[BasePermission]:
        return super().get_permissions() + [
            IsAuthenticated(),
        ]

    def retrieve(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        skill_record = skill_service.get_user_skill(
            user_id=kwargs["users_pk"],
            skill_id=kwargs["pk"],
        )
        response_serializer = self.get_serializer(
            instance=skill_record,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )

    def list(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        skill_record = skill_service.get_user_skills(
            user_id=kwargs["users_pk"],
        )
        response_serializer = self.get_serializer(
            instance=skill_record,
            many=True,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        skill_record = skill_service.create_skill_and_user_skill(
            user_id=kwargs.get("users_pk"),
            data=serializer.validated_data,
        )
        response_serializer = self.get_serializer(
            instance=skill_record,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        deleted_record = skill_service.delete_skill_and_user_skill(
            user_id=kwargs.get("users_pk"),
            skill_id=kwargs.get("pk"),
        )
        response_serializer = self.get_serializer(
            instance=deleted_record,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_204_NO_CONTENT,
        )

    def partial_update(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        updated_record = skill_service.update_skill_and_user_skill(
            user_id=kwargs.get("users_pk"),
            skill_id=kwargs.get("pk"),
            data=serializer.validated_data,
        )
        response_serializer = self.get_serializer(
            instance=updated_record,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )


user_nested_router = NestedSimpleRouter(
    parent_router=user_router,
    parent_prefix="users",
    lookup="users",
)

user_nested_router.register(
    r"skills",
    SkillViewSet,
    basename="user-skills",
)
