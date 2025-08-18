from typing import cast
from uuid import UUID

from confluent_kafka import Producer
from rest_framework.exceptions import ValidationError

from kafka.event_schemes.schemes import (
    AnalyticsEvent,
    AnalyticsEventType,
)
from kafka_initializer.apps import get_kafka_prod
from project.settings import (
    PROJECT_ANALYTICS_TOPIC,
)
from users.models import (
    UserProject,
    UserProjectRole,
)

producer = cast(Producer, get_kafka_prod())


class UserProjectRepository:
    def get_all_user_on_project(
        self,
        project_id: UUID,
    ) -> list[str]:
        """
        Return user emails that belong to the project
        """
        users = (
            UserProject.objects.filter(
                project_id=project_id,
            )
            .values_list(
                "user__email",
                flat=True,
            )
            .distinct()
        )
        return list(users)

    def get_user_project(
        self,
        user_id: UUID,
        project_id: UUID,
    ) -> UserProject | None:
        user_project = UserProject.objects.filter(
            user_id=user_id,
            project_id=project_id,
        ).first()

        if not user_project:
            return None

        return user_project

    def create_user_project(
        self,
        data: dict,
    ) -> UserProject:
        created_record = UserProject.objects.create(**data)
        event = AnalyticsEvent(
            event_type=AnalyticsEventType.PROJECT_MEMBER_ADDED,
            project_id=str(created_record.project_id),
            user_id=str(created_record.user_id),
        )
        producer.send(
            topic=PROJECT_ANALYTICS_TOPIC,
            value=event.model_dump(),
        )
        return created_record

    def update_user_project(
        self,
        user_project_id: int,
        role: UserProjectRole,
    ) -> UserProject:
        user_project = UserProject.objects.filter(pk=user_project_id).first()
        if not user_project:
            raise ValidationError("UserProject not found or already deleted")
        user_project.role = role
        user_project.save(
            update_fields=[
                "role",
            ],
        )
        return user_project


user_project_repository = UserProjectRepository()
