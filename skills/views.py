from typing import Type

from drf_spectacular.utils import extend_schema
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
)

from skills.models import (
    Skill,
)
from skills.serializers import (
    SkillSerializer,
    SkillWriteSerializer,
)

router = SimpleRouter()


@extend_schema(tags=["Skills"])
class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()

    def get_serializer_class(
        self,
    ) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return SkillSerializer
        return SkillWriteSerializer


router.register(r"", SkillViewSet, basename="skills")
