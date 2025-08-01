from django.db import transaction
from rest_framework.exceptions import ValidationError

from projects.models import Project
from projects.repositories.project_repository import (
    project_repository,
)
from users.models import (
    UserProject,
    UserProjectRole,
)
from users.repositories.user_project_repository import (
    user_project_repository,
)


class ProjectService:
    def __init__(self) -> None:
        self.repo = project_repository
        self.user_project_repo = user_project_repository

    @transaction.atomic
    def create_project(
        self,
        valid_data: dict,
    ) -> Project:
        """
        Create Project and User_Project entities
        """
        new_project = self.repo.create_project(
            data=valid_data,
        )
        user_project_data = {
            "user_id": valid_data["owner_id"],
            "project_id": new_project.id,
            "role": UserProjectRole.CREATOR,
        }
        self.add_user_to_project(
            data=user_project_data,
        )
        return new_project

    def delete_project(
        self,
        instance: Project,
    ) -> Project:
        deleted_project = self.repo.delete_project(
            deleted_project=instance,
        )
        return deleted_project

    def add_user_to_project(
        self,
        data: dict,
    ) -> UserProject:
        """
        Add a new user to an existing project
        """
        self.repo.get_project_if_not_deleted(
            project_id=data["project_id"],
        )
        if not data.get("user_id"):
            raise ValidationError("Field user_id is required")
        existing_record = self.user_project_repo.get_user_project(
            user_id=data["user_id"],
            project_id=data["project_id"],
        )
        if existing_record:
            return existing_record

        new_record = self.user_project_repo.create_user_project(
            data=data,
        )
        return new_record


project_service = ProjectService()
