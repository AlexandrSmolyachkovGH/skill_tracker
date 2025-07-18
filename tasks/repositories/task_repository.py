from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.exceptions import NotFound

from tasks.models import Task


class TaskRepository:
    def get_task(
        self,
        data: dict,
    ) -> Task:
        task = Task.objects.filter(**data).first()
        if not task:
            raise NotFound("Task not found or already deleted")
        return task

    def get_tasks(
        self,
        data: dict,
    ) -> QuerySet[Task]:
        return Task.objects.filter(**data).all()

    def get_all_tasks(self) -> QuerySet[Task]:
        return Task.objects.all()

    def create_task(
        self,
        data: dict,
    ) -> Task:
        new_task = Task.objects.create(**data)
        new_task.refresh_from_db()
        return new_task

    def partial_update_task(
        self,
        filter_data: dict,
        update_data: dict,
    ) -> Task:
        updated_task = Task.objects.filter(**filter_data).first()
        if not updated_task:
            raise NotFound("Task not found or already deleted")
        for key, value in update_data.items():
            setattr(updated_task, key, value)
        updated_task.save()
        return updated_task

    def delete_task(
        self,
        task: Task,
    ) -> Task:
        task.deleted_at = timezone.now()
        task.save()
        return task


task_repo = TaskRepository()
