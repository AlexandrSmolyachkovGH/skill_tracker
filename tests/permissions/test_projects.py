from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
)

from project.auth import RemoteJWTUser
from projects.models import (
    Project,
    ProjectStatus,
)
from projects.permissions import (
    AddToProjectPermission,
    ProjectIsNotDeletedPermission,
)
from projects.views import ProjectViewSet
from users.models import User, UserProject, UserProjectRole
from users.views import UserProjectViewSet


def create_project_with_observer_and_owner() -> tuple[User, User, Project, User]:
    """
    Create entities for testing the AddToProjectPermission
    """
    owner = User.objects.create(
        id=uuid4(),
        name="owner_user",
        email="owner_user@email.com",
    )
    observer = User.objects.create(
        id=uuid4(),
        name="observer_user",
        email="observer@email.com",
    )
    project = Project.objects.create(
        name="Project1",
        owner=owner,
    )

    UserProject.objects.create(
        user=owner,
        project=project,
    )
    UserProject.objects.create(
        user=observer,
        project=project,
        role=UserProjectRole.OBSERVER,
    )

    return owner, observer, project, User.objects.create(
        id=uuid4(),
        name="some_user",
        email="some_user@email.com",
    )


@pytest.mark.django_db
def test_add_to_project_permission(
    mock_auth_admin: RemoteJWTUser,
) -> None:
    """
    Test the AddToProjectPermission
    """
    factory = APIRequestFactory()
    _, observer, project, target_user = create_project_with_observer_and_owner()

    data = {
        "user_id": target_user.id,
        "project_id": project.id,
        "role": UserProjectRole.PARTICIPANT,
    }

    request = factory.post(
        "/api/user-projects/",
        data=data,
        format="json",
    )
    request.user = mock_auth_admin
    request.user.id = observer.id

    view = UserProjectViewSet.as_view({"post": "create"})
    response = view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["detail"] == "You do not have permission to perform this action."
