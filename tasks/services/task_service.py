from uuid import UUID

from django.db.models.query import QuerySet

from tasks.models import Task
from tasks.repositories.task_repository import task_repo


class TaskService:
    def __init__(self) -> None:
        self.repo = task_repo

    def get_task(
        self,
        task_id: UUID,
        project_id: UUID,
    ) -> Task:
        return self.repo.get_task(
            task_id=task_id,
            project_id=project_id,
        )

    def get_tasks(
        self,
        project_id: UUID,
    ) -> QuerySet[Task]:
        return self.repo.get_tasks(
            project_id=project_id,
        )

    def get_all_tasks(self) -> QuerySet[Task]:
        return self.repo.get_all_tasks()

    def create_task(
        self,
        create_data: dict,
    ) -> Task:
        new_task = self.repo.create_task(
            create_data=create_data,
        )
        return new_task

    def partial_update(
        self,
        update_data: dict,
        project_id: UUID,
        task_id: UUID,
    ) -> Task:
        updated_task = self.repo.partial_update_task(
            project_id=project_id,
            task_id=task_id,
            update_data=update_data,
        )
        return updated_task

    def delete_task(
        self,
        project_id: UUID,
        task_id: UUID,
    ) -> Task:
        deleted_task = self.repo.delete_task(
            project_id=project_id,
            task_id=task_id,
        )
        return deleted_task


task_service = TaskService()
