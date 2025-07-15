from uuid import UUID

from django.db.models.query import QuerySet
from rest_framework.request import Request

from tasks.models import Task
from tasks.repositories.task_repository import task_repo


class TaskService:
    def __init__(self) -> None:
        self.repo = task_repo

    def get_task(
        self,
        data: dict,
    ) -> Task:
        return self.repo.get_task(data=data)

    def get_tasks(
        self,
        data: dict,
    ) -> QuerySet[Task]:
        return self.repo.get_tasks(data=data)

    def get_all_tasks(self) -> QuerySet[Task]:
        return self.repo.get_all_tasks()

    def create_task(
        self,
        request: Request,
        project_id: UUID,
    ) -> Task:
        create_data = {
            "title": request.data.title,
            "status": request.data.status,
            "project": project_id,
            "assigned_to": request.user.id,
        }
        new_task = self.repo.create_task(data=create_data)
        return new_task

    def partial_update(
        self,
        request: Request,
        project_id: UUID,
        task_id: UUID,
    ) -> Task:
        filter_data = {
            "project": project_id,
            "id": task_id,
        }
        update_data = {
            key: request.data[key]
            for key in ["title", "status"]
            if key in request.data
        }
        updated_task = self.repo.partial_update_task(
            filter_data=filter_data,
            update_data=update_data,
        )
        return updated_task


task_service = TaskService()
