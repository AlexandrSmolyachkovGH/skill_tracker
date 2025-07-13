from users.models import UserProject


class UserProjectRepository:
    def create_user_project(
        self,
        data: dict,
    ) -> UserProject:
        created_record = UserProject.objects.create(**data)
        created_record.refresh_from_db()
        return created_record
