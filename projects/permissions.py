from typing import Any

from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView

from projects.models import Project
from users.models import (
    UserProject,
    UserProjectRole,
)


class AddToProjectPermission(BasePermission):
    """
    Permission to add new users to a specific project
    """

    allowed_roles = [
        UserProjectRole.CREATOR,
        UserProjectRole.MENTOR,
        UserProjectRole.PARTICIPANT,
    ]

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

        return user_project.role in self.allowed_roles


class ProjectIsNotDeletedPermission(BasePermission):
    """
    Permission to receive only not deleted projects
    """

    admin_roles = [
        "ADMIN",
        "STAFFER",
    ]

    def __init__(
        self,
        *args: Any,
        project_pk: str = "pk",
        **kwargs: Any,
    ) -> None:
        self.project_pk = project_pk
        super().__init__(*args, **kwargs)

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        project_id = view.kwargs.get(self.project_pk)
        user_role = request.user.role
        if user_role == "USER":
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return False

            if project.deleted_at:
                return False

        if user_role in self.admin_roles:
            return True

        return True
