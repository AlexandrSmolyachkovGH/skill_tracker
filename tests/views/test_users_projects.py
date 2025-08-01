from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
)

from projects.models import (
    Project,
)
from users.models import (
    User,
    UserProject,
    UserProjectRole,
)
from users.views import UserProjectViewSet


@pytest.mark.django_db
def test_get_user_project_list(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    allow_user_project_permission: MagicMock,
) -> None:
    """
    Test of receiving multiple UserProject records
    """
    factory = APIRequestFactory()

    request = factory.get("/api/user-projects/")
    request.user = mock_user_orm["auth_admin"]

    view = UserProjectViewSet.as_view({"get": "list"})
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["project_name"] == mock_project_orm.name
    assert response.data[0]["role"] == "creator"


@pytest.mark.django_db
def test_get_user_project(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    allow_user_project_permission: MagicMock,
) -> None:
    """
    Single UserProject record receiving test
    """
    factory = APIRequestFactory()

    user_project = UserProject.objects.get(
        user=mock_user_orm["user_orm"],
        project=mock_project_orm,
    )
    request = factory.get(
        f"/api/user-projects/{str(user_project.id)}/",
    )
    request.user = mock_user_orm["auth_admin"]

    view = UserProjectViewSet.as_view({"get": "retrieve"})
    response = view(
        request,
        pk=str(user_project.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["project_name"] == mock_project_orm.name
    assert response.data["role"] == "creator"


@pytest.mark.django_db
def test_create_user_project(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    allow_user_project_permission: MagicMock,
) -> None:
    """
    UserProject creation test
    """
    factory = APIRequestFactory()

    new_user = User.objects.create(
        id=uuid4(),
        name="NewUser",
        email="new_user@email.com",
    )
    data = {
        "user_id": new_user.id,
        "project_id": mock_project_orm.id,
        "role": UserProjectRole.PARTICIPANT,
    }

    request = factory.post(
        "/api/user-projects/",
        data=data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = UserProjectViewSet.as_view({"post": "create"})
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["user_id"] == str(new_user.id)
    assert response.data["role"] == UserProjectRole.PARTICIPANT


@pytest.mark.django_db
def test_delete_user_project(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    allow_user_project_permission: MagicMock,
) -> None:
    """
    UserProject deletion test
    """
    factory = APIRequestFactory()

    user_project = UserProject.objects.get(
        user=mock_user_orm["user_orm"],
        project=mock_project_orm,
    )

    request = factory.delete(
        f"/api/user-projects/{user_project.id}/",
    )
    request.user = mock_user_orm["auth_admin"]

    view = UserProjectViewSet.as_view({"delete": "destroy"})
    response = view(
        request,
        pk=str(user_project.id),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_partial_update_user_project(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    allow_user_project_permission: MagicMock,
) -> None:
    """
    UserProject partial update test
    """
    factory = APIRequestFactory()

    user_project = UserProject.objects.get(
        user=mock_user_orm["user_orm"],
        project=mock_project_orm,
    )

    new_data = {
        "role": UserProjectRole.PARTICIPANT,
    }

    request = factory.patch(
        f"/api/user-projects/{user_project.id}/",
        data=new_data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = UserProjectViewSet.as_view({"patch": "partial_update"})
    response = view(request, pk=str(user_project.id))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["role"] == new_data["role"]
