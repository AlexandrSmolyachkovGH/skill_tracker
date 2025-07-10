from rest_framework.request import Request

from users.models import User
from users.repositories.user_repository import UserRepository
from users.serializers import UserCreateSerializer


class UserService:
    def __init__(self) -> None:
        self.user_repo = UserRepository()

    def create_user(
        self,
        request: Request,
    ) -> User:
        data = dict(request.data)
        serializer = UserCreateSerializer(
            data=data,
        )
        serializer.is_valid(raise_exception=True)

        new_user = self.user_repo.create_user(
            data=serializer.validated_data,
        )
        return new_user


user_service = UserService()
