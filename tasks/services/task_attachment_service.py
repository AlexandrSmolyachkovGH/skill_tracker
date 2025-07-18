from uuid import UUID

from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from tasks.models import (
    Task,
    TaskAttachment,
)
from tasks.repositories.task_attachment_repository import (
    task_attachment_repository,
)


class TaskAttachmentService:
    def __init__(self) -> None:
        self.repo = task_attachment_repository

    def check_task_in_project(
        self,
        task_id: UUID,
        project_id: UUID,
    ) -> Task:
        try:
            task = Task.objects.get(id=task_id, project_id=project_id)
        except Task.DoesNotExist as exc:
            raise NotFound(
                "Task not found or does not belong to this project"
            ) from exc
        return task

    def create(
        self,
        task_id: UUID,
        project_id: UUID,
        request: Request,
    ) -> TaskAttachment:
        task = self.check_task_in_project(
            task_id=task_id,
            project_id=project_id,
        )
        new_attachment = self.repo.create_task_attachment(
            task=task,
            file_url=request.data["file_url"],
        )
        return new_attachment

    def update(
        self,
        attachment_id: UUID,
        task_id: UUID,
        project_id: UUID,
        request: Request,
    ) -> TaskAttachment:
        self.check_task_in_project(
            task_id=task_id,
            project_id=project_id,
        )
        try:
            attachment = TaskAttachment.objects.get(
                id=attachment_id,
                task_id=task_id,
            )
        except TaskAttachment.DoesNotExist as exc:
            raise NotFound(
                "Attachment not found or does not belong to this task"
            ) from exc
        attachment = self.repo.update_task_attachment(
            attachment=attachment,
            file_url=request.data["file_url"],
        )
        return attachment


task_attachment_service = TaskAttachmentService()
