from uuid import UUID

from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from projects.models import Project
from tasks.models import Task
from tasks.repositories.task_repository import task_repo
from users.models import User


class TaskService:
    def __init__(self) -> None:
        self.repo = task_repo

    def get_task(
        self,
        task_id: UUID,
        project_id: UUID,
    ) -> Task:
        if not isinstance(task_id, UUID):
            raise ValidationError("Invalid type task_id")
        if not isinstance(project_id, UUID):
            raise ValidationError("Invalid type project_id")
        data = {
            "id": task_id,
            "project_id": project_id,
        }
        return self.repo.get_task(data=data)

    def get_tasks(
        self,
        project_id: UUID,
    ) -> QuerySet[Task]:
        print(f"project_id: {project_id}, type: {type(project_id)}")
        if not isinstance(project_id, UUID):
            raise ValidationError("Invalid type project_id")
        data = {
            "project_id": project_id,
        }
        return self.repo.get_tasks(data=data)

    def get_all_tasks(self) -> QuerySet[Task]:
        return self.repo.get_all_tasks()

    def create_task(
        self,
        request: Request,
        project_id: UUID,
    ) -> Task:
        user = get_object_or_404(User, id=request.user.id)
        project = get_object_or_404(Project, id=project_id)
        create_data = {
            "title": request.data["title"],
            "status": request.data["status"],
            "project": project,
            "assigned_to": user,
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

    def delete_task(
        self,
        project_id: UUID,
        task_id: UUID,
    ) -> Task:
        task = get_object_or_404(Task, id=task_id)
        if str(task.project.id) != project_id:
            raise ValidationError("Invalid project id")
        if task.deleted_at:
            raise ValidationError("Task has already been deleted")
        deleted_task = self.repo.delete_task(
            task=task,
        )
        return deleted_task


task_service = TaskService()
