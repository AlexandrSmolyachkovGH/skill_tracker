from typing import (
    Any,
    Type,
)

from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
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
from projects.permissions import AddToProjectPermission
from projects.serializers import (
    AddToProjectSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
    ProjectWriteSerializer,
)
from projects.services.project_service import project_service
from tasks.views import TaskViewSet
from users.models import UserProjectRole
from users.serializers import UserProjectSerializer

router = DefaultRouter()


class ProjectPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(tags=["Projects"])
class ProjectViewSet(ModelViewSet):
    pagination_class = ProjectPagination

    def get_queryset(
        self,
    ) -> QuerySet[Project]:
        if self.request.user.role in ["USER"]:
            user_id = self.request.user.id
            return Project.objects.filter(project_users__user_id=user_id).all()
        return Project.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
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
        new_project = project_service.create_project(
            request=request,
        )
        response_serializer = ProjectSerializer(new_project)
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
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
        project = self.get_object()
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
        response_serializer = UserProjectSerializer(new_record)
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


router.register(r"", ProjectViewSet, basename="projects")

project_router = NestedSimpleRouter(
    parent_router=router,
    parent_prefix="",
    lookup="projects",
)
project_router.register(r"tasks", TaskViewSet, basename="tasks")
