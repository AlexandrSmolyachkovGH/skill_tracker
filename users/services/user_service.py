from uuid import UUID

from users.models import User
from users.repositories.user_repository import user_repository


class UserService:
    def __init__(self) -> None:
        self.user_repo = user_repository

    def create_user(
        self,
        data: dict,
    ) -> User:
        new_user = self.user_repo.create_user(
            data=data,
        )
        return new_user

    def delete_user(
        self,
        user_id: UUID,
    ) -> User:
        deleted_user = self.user_repo.delete_user(
            user_id=user_id,
        )
        return deleted_user

    def update_user(
        self,
        user_id: UUID,
        name: str,
    ) -> User:
        user_record = self.user_repo.update_user(
            user_id=user_id,
            name=name,
        )
        return user_record


user_service = UserService()
