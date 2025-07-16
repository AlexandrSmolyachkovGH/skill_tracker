from typing import (
    Any,
    Type,
)

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

from tasks.models import (
    Task,
    TaskAttachment,
)
from tasks.permissions import OwnerOrAdminPermission
from tasks.serializers import (
    TaskAttachmentSerializer,
    TaskAttachmentWriteSerializer,
    TaskCreateSerializer,
    TaskPartialUpdateSerializer,
    TaskSerializer,
    TaskWriteSerializer,
)
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
        return super().get_permissions()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return TaskSerializer
        if self.action in ["create"]:
            return TaskCreateSerializer
        if self.action in ["partial_update"]:
            return TaskPartialUpdateSerializer
        return TaskWriteSerializer

    def retrieve(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        task = task_service.get_task(
            task_id=kwargs["pk"],
            project_id=kwargs["projects_pk"],
        )
        response_serializer = self.get_serializer(instance=task)
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
            project_id=kwargs["projects_pk"],
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
            isinstance=updated_task,
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
    queryset = TaskAttachment.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return TaskAttachmentSerializer
        return TaskAttachmentWriteSerializer


router.register(r"all-tasks", AllTasksViewSet, basename="all-tasks")
# router.register(
#     r"attachments", TaskAttachmentViewSet, basename="task-attachments"
# )
