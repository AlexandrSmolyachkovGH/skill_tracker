from typing import Type

from drf_spectacular.utils import extend_schema
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
)

from projects.models import (
    Project,
)
from projects.serializers import (
    ProjectSerializer,
    ProjectWriteSerializer,
)

router = SimpleRouter()


@extend_schema(tags=["Projects"])
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return ProjectSerializer
        return ProjectWriteSerializer


router.register(r"", ProjectViewSet, basename="projects")
