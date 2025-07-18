from typing import (
    Any,
    Type,
)
from uuid import UUID

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
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
    UserCreateSerializer,
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
    pagination_class = UserPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["created_at", "name"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self) -> QuerySet[User]:
        user = self.request.user
        if user.role in ["USER"]:
            queryset = User.objects.filter(id=user.id)
            return queryset
        return User.objects.all()

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
        if self.action in ["list", "retrieve", "destroy"]:
            return UserSerializer
        if self.action in ["create"]:
            return UserCreateSerializer
        return UserWriteSerializer

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
        user_record = user_service.create_user(
            data=serializer.data,
        )
        response_serializer = self.get_serializer(
            instance=user_record,
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
        deleted_record = user_service.delete_user(
            user_id=UUID(kwargs.get("pk")),
        )
        response_serializer = self.get_serializer(
            instance=deleted_record,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
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
        user_record = user_service.update_user(
            request=request,
        )
        response_serializer = self.get_serializer(
            instance=user_record,
        )
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

    def get_queryset(self) -> QuerySet[User]:
        # user = self.request.user
        # print("DEBUG: inside get_queryset")
        # if user.role in ["USER"]:
        #     print("DEBUG: IF get_queryset")
        #     queryset = UserProject.objects.filter(user_id=user.id)
        #     return queryset
        return UserProject.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return UserProjectSerializer
        return UserProjectWriteSerializer

    # def list(self, request, *args, **kwargs):
    #     lst = UserProject.objects.filter(user_id=request.user.id)
    #     return Response(
    #         data=lst,
    #         status=status.HTTP_200_OK,
    #     )


router.register(r"", UserViewSet, basename="users")
router.register(r"skills", UserSkillViewSet, basename="user-skills")

user_project_router = DefaultRouter()
user_project_router.register(r"", UserProjectViewSet, basename="user-projects")
