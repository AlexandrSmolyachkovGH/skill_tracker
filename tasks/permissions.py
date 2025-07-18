from typing import Any

from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView

from tasks.models import Task
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


class TaskIsNotDeletedPermission(BasePermission):
    """
    Permission to receive only not deleted tasks
    """

    def __init__(
        self,
        *args: Any,
        task_pk: str = "pk",
        **kwargs: Any,
    ) -> None:
        self.task_pk = task_pk
        super().__init__(*args, **kwargs)

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        task_id = view.kwargs.get(self.task_pk)
        if not task_id:
            return False

        if request.user.role == "USER":
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return False

            if task.deleted_at:
                return False

        return True
