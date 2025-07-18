from rest_framework.request import Request

from users.models import UserProject, UserProjectRole
from users.repositories.user_project_repository import UserProjectRepository
from users.serializers import UserProjectWriteSerializer


class UserProjectService:
    def __init__(
        self,
    ) -> None:
        self.repo = UserProjectRepository()

    def create_user_project(
        self,
        data: dict,
    ) -> UserProject:
        """
        Create a UserProject entity
        """
        user_project_serializer = UserProjectWriteSerializer(
            data=data,
        )
        user_project_serializer.is_valid(raise_exception=True)
        new_record = self.repo.create_user_project(
            data=user_project_serializer.validated_data,
        )
        return new_record

    def update_user_project(
        self,
        user_project_id: int,
        request: Request,
    ) -> UserProject:
        role = request.data["role"]
        updated_user = self.repo.update_user_project(
            user_project_id=user_project_id,
            role=role,
        )
        return updated_user


user_project_service = UserProjectService()
