from typing import (
    Any,
    Type,
)
from uuid import UUID

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
)

from projects.permissions import (
    ProjectIsNotDeletedPermission,
)
from tasks.models import (
    TaskAttachment,
)
from tasks.permissions import (
    OwnerOrAdminPermission,
    TaskIsNotDeletedPermission,
)
from tasks.serializers import (
    TaskAttachmentSerializer,
    TaskAttachmentWriteSerializer,
    TaskCreateSerializer,
    TaskPartialUpdateSerializer,
    TaskSerializer,
)
from tasks.services.task_attachment_service import task_attachment_service
from tasks.services.task_service import task_service

router = DefaultRouter()


class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(tags=["Tasks"])
class TaskViewSet(ModelViewSet):
    pagination_class = TaskPagination
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_fields = ["title", "status"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]

    def get_permissions(self) -> list[BasePermission]:
        if self.action == 'destroy':
            return [OwnerOrAdminPermission()]
        if self.action in ['partial_update']:
            return [
                TaskIsNotDeletedPermission(task_pk="pk"),
                ProjectIsNotDeletedPermission(project_pk="projects_pk"),
            ]
        return super().get_permissions()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve", "destroy"]:
            return TaskSerializer
        if self.action in ["create"]:
            return TaskCreateSerializer
        if self.action in ["partial_update"]:
            return TaskPartialUpdateSerializer
        return TaskSerializer

    def retrieve(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        task = task_service.get_task(
            task_id=UUID(kwargs["pk"]),
            project_id=UUID(kwargs["projects_pk"]),
        )
        response_serializer = self.get_serializer(
            instance=task,
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
        tasks = task_service.get_tasks(
            project_id=UUID(
                kwargs["projects_pk"],
            ),
        )
        response_serializer = TaskSerializer(
            instance=tasks,
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
        new_task = task_service.create_task(
            request=request,
            project_id=kwargs["projects_pk"],
        )
        response_serializer = self.get_serializer(
            instance=new_task,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Update only task title and/or status
        """
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        updated_task = task_service.partial_update(
            request=request,
            project_id=kwargs["projects_pk"],
            task_id=kwargs["pk"],
        )
        response_serializer = self.get_serializer(
            instance=updated_task,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )

    def destroy(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        deleted_task = task_service.delete_task(
            task_id=kwargs["pk"],
            project_id=kwargs["projects_pk"],
        )
        response_serializer = self.get_serializer(
            instance=deleted_task,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Tasks"])
class AllTasksViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = TaskPagination
    http_method_names = ["get"]
    serializer_class = TaskSerializer
    filterset_fields = ["title", "status"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]

    def list(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Return a list of all tasks
        """
        all_tasks = task_service.get_all_tasks()
        response_serializer = self.serializer_class(
            all_tasks,
            many=True,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Task-Attachments"])
class TaskAttachmentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self) -> list[BasePermission]:
        if self.action == 'destroy':
            return [OwnerOrAdminPermission()]
        if self.action in ['partial_update']:
            return [
                TaskIsNotDeletedPermission(task_pk="tasks_pk"),
                ProjectIsNotDeletedPermission(project_pk="projects_pk"),
            ]
        return super().get_permissions()

    def get_queryset(
        self,
    ) -> QuerySet[TaskAttachment]:
        if self.request.user.role in ["USER"]:
            user_id = self.request.user.id
            return TaskAttachment.objects.filter(
                task__project__project_users__user_id=user_id,
            ).all()
        return TaskAttachment.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve", "destroy"]:
            return TaskAttachmentSerializer
        return TaskAttachmentWriteSerializer

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
        new_attachment = task_attachment_service.create(
            request=request,
            project_id=kwargs["projects_pk"],
            task_id=kwargs["tasks_pk"],
        )
        response_serializer = self.get_serializer(
            instance=new_attachment,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
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
        attachment = task_attachment_service.update(
            request=request,
            attachment_id=kwargs["pk"],
            project_id=kwargs["projects_pk"],
            task_id=kwargs["tasks_pk"],
        )
        response_serializer = self.get_serializer(
            instance=attachment,
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )


router.register(
    r"all-tasks",
    AllTasksViewSet,
    basename="all-tasks",
)
