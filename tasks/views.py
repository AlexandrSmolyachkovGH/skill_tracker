from typing import (
    Any,
    Type,
)

from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
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


@extend_schema(tags=["Tasks"])
class TaskViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_fields = ["title", "status"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]

    def get_queryset(
        self,
    ) -> QuerySet[Task]:
        if self.request.user.role in ["USER"]:
            user_id = self.request.user.id
            return Task.objects.filter(
                project__projectmembership__user_id=user_id
            )
        return Task.objects.all()

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
        task_id = kwargs.get("pk")
        project_id = kwargs.get("projects_pk")
        data = {
            "id": task_id,
            "project_id": project_id,
        }
        task = task_service.get_task(
            data=data,
        )
        response_serializer = TaskSerializer(task)
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
        data = {"project_id": kwargs.get("projects_pk")}
        tasks = task_service.get_tasks(
            data=data,
        )
        response_serializer = TaskSerializer(tasks, many=True)
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
        new_task = task_service.create_task(
            request=request,
            project_id=kwargs["projects_pk"],
        )
        response_serializer = TaskSerializer(new_task)
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
        Update only task title and/or status.
        """
        updated_task = task_service.partial_update(
            request=request,
            project_id=kwargs["projects_pk"],
            task_id=kwargs["pk"],
        )
        response_serializer = TaskSerializer(updated_task)
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )

    # @action(
    #     methods=["get"],
    #     detail=False,
    #     url_path="get-all-projects-tasks",
    #     permission_classes=[IsAuthenticated],
    # )
    # def get_all_projects_tasks(
    #     self,
    #     request: Request,
    #     *args: Any,
    #     **kwargs: Any,
    # ) -> Response:
    #     queryset = Task.objects.all()
    #     all_tasks = task_service.get_all_tasks()
    #     response_serializer = TaskSerializer(all_tasks, many=True)
    #     return Response(
    #         data=response_serializer.data,
    #         status=status.HTTP_200_OK,
    #     )


@extend_schema(tags=["Task-Attachments"])
class TaskAttachmentViewSet(ModelViewSet):
    queryset = TaskAttachment.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return TaskAttachmentSerializer
        return TaskAttachmentWriteSerializer


# router.register(r"", TaskViewSet, basename="tasks")
router.register(
    r"attachments/", TaskAttachmentViewSet, basename="task-attachments"
)
