from django.utils import timezone

from projects.models import Project


class ProjectRepository:
    def create_project(self, data: dict) -> Project:
        created_project = Project.objects.create(**data)
        created_project.refresh_from_db()
        return created_project

    def delete_project(self, deleted_project: Project) -> Project:
        deleted_project.deleted_at = timezone.now()
        deleted_project.save(
            update_fields=["deleted_at"],
        )
        return deleted_project
