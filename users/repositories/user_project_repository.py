from uuid import UUID

from rest_framework.exceptions import ValidationError

from users.models import (
    UserProject,
    UserProjectRole,
)


class UserProjectRepository:
    def get_user_project(
        self,
        user_id: UUID,
        project_id: UUID,
    ) -> UserProject | None:
        user_project = UserProject.objects.filter(
            user_id=user_id,
            project_id=project_id,
        ).first()

        if not user_project:
            return None

        return user_project

    def create_user_project(
        self,
        data: dict,
    ) -> UserProject:
        created_record = UserProject.objects.create(**data)
        return created_record

    def update_user_project(
        self,
        user_project_id: int,
        role: UserProjectRole,
    ) -> UserProject:
        user_project = UserProject.objects.filter(pk=user_project_id).first()
        if not user_project:
            raise ValidationError("UserProject not found or already deleted")
        user_project.role = role
        user_project.save(
            update_fields=[
                "role",
            ],
        )
        return user_project


user_project_repository = UserProjectRepository()
