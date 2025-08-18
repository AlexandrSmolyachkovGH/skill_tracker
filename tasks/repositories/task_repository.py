import json
from typing import cast
from uuid import (
    UUID,
    uuid4,
)

from confluent_kafka import Producer
from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.exceptions import (
    NotFound,
)

from kafka.event_schemes.schemes import (
    AnalyticsEvent,
)
from kafka.event_schemes.schemes import AnalyticsEventType as EventType
from kafka_initializer.apps import get_kafka_prod
from project.settings import (
    PROJECT_ANALYTICS_TOPIC,
)
from tasks.models import (
    Task,
    TaskStatus,
)
from utils.connections.conn_redis import redis_db

producer = cast(Producer, get_kafka_prod())


class TaskRepository:
    def check_and_return_task_if_exists(
        self,
        task_id: UUID,
        project_id: UUID,
    ) -> Task:
        try:
            task = Task.objects.get(
                id=task_id,
                project_id=project_id,
            )
        except Task.DoesNotExist as exc:
            raise NotFound(
                "Task not found or does not belong to this project"
            ) from exc
        return task

    def check_and_return_task_if_not_deleted(
        self,
        task: Task,
    ) -> Task:
        if task.deleted_at:
            raise NotFound("The Task has already been deleted")
        return task

    def get_task(
        self,
        task_id: UUID,
        project_id: UUID,
    ) -> Task:
        task = self.check_and_return_task_if_exists(
            task_id=task_id,
            project_id=project_id,
        )
        return task

    def get_tasks(
        self,
        project_id: UUID,
    ) -> QuerySet[Task]:
        return Task.objects.filter(project_id=project_id).all()

    def get_all_tasks(self) -> QuerySet[Task]:
        return Task.objects.all()

    def create_task(
        self,
        create_data: dict,
    ) -> Task:
        new_task = Task.objects.create(**create_data)

        event = AnalyticsEvent(
            event_type=EventType.TASK_CREATED,
            user_id=str(new_task.assigned_to_id),
            project_id=str(new_task.project_id),
            task_id=str(new_task.id),
        )

        producer.send(
            topic=PROJECT_ANALYTICS_TOPIC,
            value=event.model_dump(),
        )

        return new_task

    def partial_update_task(
        self,
        task_id: UUID,
        project_id: UUID,
        update_data: dict,
    ) -> Task:
        task = self.check_and_return_task_if_exists(
            task_id=task_id,
            project_id=project_id,
        )
        self.check_and_return_task_if_not_deleted(task=task)
        old_status = task.status

        for key, value in update_data.items():
            setattr(task, key, value)
        task.save(
            update_fields=list(update_data.keys()),
        )
        upd_status = update_data.get("status", None)

        if upd_status and old_status != upd_status:
            redis_db.set(
                name="update_status:" + str(uuid4()),
                value=json.dumps(
                    {
                        "task_id": str(task.id),
                        "project_id": str(task.project_id),
                        "status": upd_status,
                    }
                ),
                ex=600,
            )

            events = []

            event = AnalyticsEvent(
                event_type=EventType.TASK_STATUS_CHANGED,
                user_id=str(task.assigned_to_id),
                project_id=str(task.project_id),
                task_id=str(task.id),
            )

            events.append(event)

            if upd_status == TaskStatus.COMPLETED:
                event_complete = AnalyticsEvent(
                    event_type=EventType.TASK_COMPLETED,
                    user_id=str(task.assigned_to_id),
                    project_id=str(task.project_id),
                    task_id=str(task.id),
                )

                events.append(event_complete)

            for event in events:
                producer.send(
                    topic=PROJECT_ANALYTICS_TOPIC,
                    value=event.model_dump(),
                )

        return task

    def delete_task(
        self,
        project_id: UUID,
        task_id: UUID,
    ) -> Task:
        task = self.check_and_return_task_if_exists(
            task_id=task_id,
            project_id=project_id,
        )
        self.check_and_return_task_if_not_deleted(task=task)
        task.deleted_at = timezone.now()
        task.save(
            update_fields=[
                "deleted_at",
            ],
        )
        return task


task_repo = TaskRepository()
