from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView

from project.settings import SERVICE_SECRET


class InternalSecretPermission(BasePermission):
    """
    Permission to create user only if secret key has been provided
    """

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        if request.method in ["POST", "DELETE"] and getattr(
            view, "action", None
        ) in [
            "create",
            "destroy",
        ]:
            secret = request.headers.get("Service-Secret")
            return secret == SERVICE_SECRET
        return True
