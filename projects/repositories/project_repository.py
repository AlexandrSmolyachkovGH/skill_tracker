from typing import cast
from uuid import UUID

from confluent_kafka import Producer
from django.utils import timezone
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
)

from kafka.event_schemes.schemes import (
    AnalyticsEvent,
    AnalyticsEventType,
)
from kafka_initializer.apps import get_kafka_prod
from project.settings import (
    PROJECT_ANALYTICS_TOPIC,
)
from projects.models import Project

producer = cast(Producer, get_kafka_prod())


class ProjectRepository:
    def create_project(self, data: dict) -> Project:
        created_project = Project.objects.create(**data)

        event = AnalyticsEvent(
            event_type=AnalyticsEventType.PROJECT_CREATED,
            user_id=str(created_project.owner_id),
            project_id=str(created_project.id),
        )

        producer.send(
            topic=PROJECT_ANALYTICS_TOPIC,
            value=event.model_dump(),
        )
        return created_project

    def delete_project(self, deleted_project: Project) -> Project:
        if deleted_project.deleted_at:
            raise ValidationError("Project has already been deleted")
        deleted_project.deleted_at = timezone.now()
        deleted_project.save(
            update_fields=["deleted_at"],
        )
        return deleted_project

    def get_project_if_not_deleted(
        self,
        project_id: UUID,
    ) -> Project:
        project = Project.objects.filter(id=project_id).first()
        if not project:
            raise NotFound("Project not found")
        if project.deleted_at:
            raise ValidationError("Project has already been deleted")
        return project


project_repository = ProjectRepository()
