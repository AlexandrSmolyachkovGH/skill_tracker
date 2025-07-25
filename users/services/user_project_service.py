from users.models import (
    UserProject,
    UserProjectRole,
)
from users.repositories.user_project_repository import user_project_repository


class UserProjectService:
    def __init__(
        self,
    ) -> None:
        self.repo = user_project_repository

    def update_user_project(
        self,
        user_project_id: int,
        role: UserProjectRole,
    ) -> UserProject:
        """
        Update a UserProject entity
        """
        updated_user = self.repo.update_user_project(
            user_project_id=user_project_id,
            role=role,
        )
        return updated_user


user_project_service = UserProjectService()
