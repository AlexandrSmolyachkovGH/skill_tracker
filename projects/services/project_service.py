from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from projects.models import Project
from projects.repositories.project_repository import ProjectRepository
from users.models import (
    UserProject,
    UserProjectRole,
)
from users.services.user_project_service import user_project_service


class ProjectService:
    def __init__(self) -> None:
        self.repo = ProjectRepository()
        self.user_project_service = user_project_service

    @transaction.atomic
    def create_project(
        self,
        valid_data: dict,
        request: Request,
    ) -> Project:
        """
        Create Project and User_Project entities
        """
        owner_data = {
            "owner_id": request.user.id,
        }
        valid_data.update(owner_data)
        new_project = self.repo.create_project(
            data=valid_data,
        )
        user_project_data = {
            "user_id": request.user.id,
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
        if instance.deleted_at:
            raise ValidationError("Project has already been deleted")
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
        if not data["user_id"]:
            raise ValidationError("Field user_id is required")
        new_record = self.user_project_service.create_user_project(
            data=data,
        )
        return new_record


project_service = ProjectService()
