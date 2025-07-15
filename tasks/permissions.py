from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView

from users.models import (
    UserProject,
    UserProjectRole,
)


class OwnerOrAdminPermission(BasePermission):
    """
    Permission to a specific project
    """

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Check user access to a specific project.
        """
        admin_roles = [
            UserProjectRole.CREATOR,
            UserProjectRole.MENTOR,
            UserProjectRole.PARTICIPANT,
        ]
        if request.user.role in admin_roles:
            return True

        project_id = view.kwargs.get("projects_pk")
        user_id = request.user.id

        try:
            UserProject.objects.get(
                user_id=user_id,
                project_id=project_id,
            )
            return True
        except UserProject.DoesNotExist:
            return False
