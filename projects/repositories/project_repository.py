from projects.models import Project


class ProjectRepository:
    def create_project(self, data: dict) -> Project:
        created_project = Project.objects.create(**data)
        created_project.refresh_from_db()
        return created_project
