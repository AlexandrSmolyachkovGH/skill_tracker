from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView

from users.models import (
    UserProject,
    UserProjectRole,
)


class AddToProjectPermission(BasePermission):
    """
    Permission to add new users to a specific project
    """

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        project_id = view.kwargs.get("pk")
        user_id = request.user.id

        try:
            user_project = UserProject.objects.get(
                user_id=user_id,
                project_id=project_id,
            )
        except UserProject.DoesNotExist:
            return False

        allowed_roles = [
            UserProjectRole.CREATOR,
            UserProjectRole.MENTOR,
            UserProjectRole.PARTICIPANT,
        ]

        return user_project.role in allowed_roles
