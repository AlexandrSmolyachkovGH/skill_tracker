from uuid import UUID

from rest_framework.exceptions import (
    NotFound,
)

from tasks.models import (
    Task,
    TaskAttachment,
)


class TaskAttachmentRepository:
    def __init__(self) -> None:
        self.pending_url: str = "waiting for loading"

    def get_attachment_by_id(
        self,
        attachment_id: UUID,
    ) -> TaskAttachment:
        try:
            attachment = TaskAttachment.objects.get(
                id=attachment_id,
            )
        except TaskAttachment.DoesNotExist as exc:
            raise NotFound("Attachment not found") from exc

        return attachment

    def get_attachment_if_exists(
        self,
        task_id: UUID,
        attachment_id: UUID,
    ) -> TaskAttachment:
        try:
            attachment = TaskAttachment.objects.get(
                id=attachment_id,
                task_id=task_id,
            )
        except TaskAttachment.DoesNotExist as exc:
            raise NotFound(
                "Attachment not found or does not belong to this task"
            ) from exc

        return attachment

    def create_task_attachment(
        self,
        task: Task,
    ) -> TaskAttachment:
        attachment = TaskAttachment.objects.create(
            file_url=self.pending_url,
            task=task,
        )
        return attachment

    def update_task_attachment(
        self,
        attachment: TaskAttachment,
        file_url: str,
    ) -> TaskAttachment:
        attachment.file_url = file_url
        attachment.save(
            update_fields=[
                "file_url",
            ],
        )
        return attachment


task_attachment_repository = TaskAttachmentRepository()
