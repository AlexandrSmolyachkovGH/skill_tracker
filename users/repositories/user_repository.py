from users.models import User


class UserRepository:
    def create_user(self, data: dict) -> User:
        created_user = User.objects.create(**data)
        created_user.refresh_from_db()
        return created_user
