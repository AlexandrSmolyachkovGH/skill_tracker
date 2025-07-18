from uuid import UUID

from django.utils import timezone
from rest_framework.exceptions import NotFound

from users.models import User


class UserRepository:
    def create_user(
        self,
        data: dict,
    ) -> User:
        created_user = User.objects.create(**data)
        created_user.refresh_from_db()
        return created_user

    def delete_user(
        self,
        user_id: UUID,
    ) -> User:
        deleted_user = User.objects.filter(id=user_id).first()
        if not deleted_user:
            raise NotFound("User not found or already deleted")
        deleted_user.deleted_at = timezone.now()
        deleted_user.email = "deleted_" + deleted_user.email
        deleted_user.name = "deleted_" + deleted_user.name
        deleted_user.save()
        deleted_user.refresh_from_db()
        return deleted_user

    def update_user(
        self,
        user_id: UUID,
        name: str,
    ) -> User:
        updated_user = User.objects.filter(id=user_id).first()
        if not updated_user:
            raise NotFound("User not found or already updated")
        updated_user.name = name
        updated_user.save()
        return updated_user
