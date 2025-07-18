from rest_framework.exceptions import ValidationError

from users.models import (
    UserProject,
    UserProjectRole,
)


class UserProjectRepository:
    def create_user_project(
        self,
        data: dict,
    ) -> UserProject:
        created_record = UserProject.objects.create(**data)
        created_record.refresh_from_db()
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
        user_project.save()
        return user_project
