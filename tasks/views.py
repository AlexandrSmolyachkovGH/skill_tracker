from typing import Type

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
)

from tasks.models import (
    Task,
    TaskAttachment,
)
from tasks.serializers import (
    TaskAttachmentSerializer,
    TaskAttachmentWriteSerializer,
    TaskSerializer,
    TaskWriteSerializer,
)

router = SimpleRouter()


@extend_schema(tags=["Tasks"])
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return TaskSerializer
        return TaskWriteSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'project']
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']


@extend_schema(tags=["Task-Attachments"])
class TaskAttachmentViewSet(ModelViewSet):
    queryset = TaskAttachment.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return TaskAttachmentSerializer
        return TaskAttachmentWriteSerializer


router.register(r"", TaskViewSet, basename="tasks")
router.register(
    r"attachments/", TaskAttachmentViewSet, basename="task-attachments"
)
