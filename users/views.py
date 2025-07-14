from typing import (
    Any,
    Type,
)
from uuid import UUID

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
)

from project.auth import (
    NoAuth,
    RemoteJWTAuthentication,
)
from users.models import (
    User,
    UserProject,
    UserSkill,
)
from users.permissions import InternalSecretPermission
from users.serializers import (
    UserProjectSerializer,
    UserProjectWriteSerializer,
    UserSerializer,
    UserSkillSerializer,
    UserSkillWriteSerializer,
    UserWriteSerializer,
)
from users.services.user_service import user_service

router = DefaultRouter()


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(tags=["Users"])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserWriteSerializer
    pagination_class = UserPagination

    def get_queryset(self) -> QuerySet[User]:
        user = self.request.user
        if user.role in ["USER"]:
            queryset = self.queryset.filter(id=user.id)
            return queryset
        return self.queryset

    def get_authenticators(
        self,
    ) -> list[BaseAuthentication]:
        if getattr(self, "action", None) in ["create", "destroy"]:
            return [NoAuth()]
        return [RemoteJWTAuthentication()]

    def get_permissions(
        self,
    ) -> list[BasePermission]:
        if self.action in ["create", "destroy"]:
            return [InternalSecretPermission()]
        return [IsAuthenticated()]

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return UserSerializer
        return UserWriteSerializer

    def create(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        print("hello from Create")
        user_record = user_service.create_user(
            request=request,
        )
        response_serializer = UserSerializer(user_record)
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
        print("hello from Destroy")
        user_id = kwargs.get("pk")
        deleted_record = user_service.delete_user(
            user_id=UUID(user_id),
        )
        response_serializer = UserSerializer(deleted_record)
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )


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
