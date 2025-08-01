from uuid import UUID

from tasks.models import (
    TaskAttachment,
)
from tasks.repositories.task_attachment_repository import (
    task_attachment_repository,
)
from tasks.repositories.task_repository import task_repo


class TaskAttachmentService:
    def __init__(self) -> None:
        self.repo = task_attachment_repository
        self.task_repo = task_repo

    def create(
        self,
        task_id: UUID,
        project_id: UUID,
        valid_data: dict,
    ) -> TaskAttachment:
        task = self.task_repo.check_and_return_task_if_exists(
            task_id=task_id,
            project_id=project_id,
        )
        new_attachment = self.repo.create_task_attachment(
            task=task,
            file_url=valid_data["file_url"],
        )
        return new_attachment

    def update(
        self,
        attachment_id: UUID,
        task_id: UUID,
        project_id: UUID,
        file_url: str,
    ) -> TaskAttachment:
        self.task_repo.check_and_return_task_if_exists(
            task_id=task_id,
            project_id=project_id,
        )
        attachment = self.repo.get_attachment_if_exists(
            task_id=task_id,
            attachment_id=attachment_id,
        )
        updated_attachment = self.repo.update_task_attachment(
            attachment=attachment,
            file_url=file_url,
        )
        return updated_attachment


task_attachment_service = TaskAttachmentService()
