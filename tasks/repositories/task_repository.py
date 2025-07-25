from uuid import UUID

from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.exceptions import (
    NotFound,
)

from tasks.models import Task


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
        for key, value in update_data.items():
            setattr(task, key, value)
        task.save(
            update_fields=list(update_data.keys()),
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
