from tasks.models import (
    Task,
    TaskAttachment,
)


class TaskAttachmentRepository:
    def create_task_attachment(
        self,
        task: Task,
        file_url: str,
    ) -> TaskAttachment:
        attachment = TaskAttachment.objects.create(
            file_url=file_url,
            task=task,
        )
        return attachment

    def update_task_attachment(
        self,
        attachment: TaskAttachment,
        file_url: str,
    ) -> TaskAttachment:
        attachment.file_url = file_url
        attachment.save()
        return attachment


task_attachment_repository = TaskAttachmentRepository()
