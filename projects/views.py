from typing import (
    Any,
    Type,
)

from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
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
from rest_framework_nested.routers import NestedSimpleRouter

from projects.models import (
    Project,
)
from projects.permissions import (
    AddToProjectPermission,
    ProjectIsNotDeletedPermission,
)
from projects.serializers import (
    AddToProjectSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
    ProjectWriteSerializer,
)
from projects.services.project_service import project_service
from tasks.views import (
    TaskAttachmentViewSet,
    TaskViewSet,
)
from users.models import UserProjectRole

router = DefaultRouter()


class ProjectPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(tags=["Projects"])
class ProjectViewSet(ModelViewSet):
    pagination_class = ProjectPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_fields = ["name", "status"]
    search_fields = ["name"]
    ordering_fields = ["created_at", "name"]

    def get_queryset(
        self,
    ) -> QuerySet[Project]:
        if self.request.user.role in ["USER"]:
            user_id = self.request.user.id
            return Project.objects.filter(project_users__user_id=user_id).all()
        return Project.objects.all()

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ["update", "partial_update"]:
            return [
                ProjectIsNotDeletedPermission(
                    project_pk="pk",
                )
            ]
        return super().get_permissions()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve", "destroy"]:
            return ProjectSerializer
        if self.action == "create":
            return ProjectCreateSerializer
        if self.action == "add_user_to_project":
            return AddToProjectSerializer
        return ProjectWriteSerializer

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
        new_project = project_service.create_project(
            valid_data=serializer.validated_data,
            request=request,
        )
        response_serializer = self.get_serializer(
            instance=new_project,
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
        """
        Soft delete for a project
        """
        instance = self.get_object()
        deleted_project = project_service.delete_project(
            instance=instance,
        )
        serializer = self.get_serializer(
            instance=deleted_project,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="add-user",
        permission_classes=[
            IsAuthenticated,
            AddToProjectPermission,
        ],
    )
    def add_user_to_project(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Add new user to the project
        """
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        project = self.get_object()
        if project.deleted_at:
            raise ValidationError("Project has already been deleted")
        project_id = project.id
        user_id = request.data.get("user_id", None)
        role = request.data.get("role", UserProjectRole.OBSERVER)

        new_record = project_service.add_user_to_project(
            data={
                "user_id": user_id,
                "project_id": project_id,
                "role": role,
            }
        )
        response_serializer = self.get_serializer(
            instance=new_record,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


router.register(
    r"",
    ProjectViewSet,
    basename="projects",
)

project_router = NestedSimpleRouter(
    parent_router=router,
    parent_prefix="",
    lookup="projects",
)
project_router.register(
    r"tasks",
    TaskViewSet,
    basename="tasks",
)

task_router = NestedSimpleRouter(
    parent_router=project_router,
    parent_prefix="tasks",
    lookup="tasks",
)
task_router.register(
    r"attachments",
    TaskAttachmentViewSet,
    basename="attachments",
)
