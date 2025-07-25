from unittest.mock import MagicMock

import pytest
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
)

from projects.models import (
    Project,
    ProjectStatus,
)
from projects.views import ProjectViewSet


@pytest.mark.django_db
def test_get_project_list(
    mock_user_orm: dict,
    allow_any_permission: MagicMock,
    mock_project_orm: Project,
) -> None:
    """
    Test of receiving multiple project records
    """
    factory = APIRequestFactory()

    request = factory.get("/api/projects/")
    request.user = mock_user_orm["auth_admin"]

    view = ProjectViewSet.as_view({"get": "list"})
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == mock_project_orm.name
    assert response.data["results"][0]["status"] == mock_project_orm.status


@pytest.mark.django_db
def test_get_project(
    mock_user_orm: dict,
    allow_any_permission: MagicMock,
    mock_project_orm: Project,
) -> None:
    """
    Single project record receiving test
    """
    factory = APIRequestFactory()

    request = factory.get(f"/api/projects/{mock_project_orm.id}/")
    request.user = mock_user_orm["auth_admin"]

    view = ProjectViewSet.as_view({"get": "retrieve"})
    response = view(request, pk=str(mock_project_orm.id))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(mock_project_orm.id)
    assert response.data["name"] == mock_project_orm.name
    assert response.data["status"] == mock_project_orm.status


@pytest.mark.django_db
def test_create_project(
    mock_user_orm: dict,
    allow_any_permission: MagicMock,
) -> None:
    """
    Project creation test
    """
    factory = APIRequestFactory()

    data = {
        "name": "Project1",
        "status": ProjectStatus.ACTIVE,
    }

    request = factory.post(
        "/api/projects/",
        data=data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = ProjectViewSet.as_view({"post": "create"})
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert response.data["status"] == ProjectStatus.ACTIVE


@pytest.mark.django_db
def test_delete_project(
    mock_user_orm: dict,
    allow_any_permission: MagicMock,
    mock_project_orm: Project,
) -> None:
    """
    Project deletion test
    """
    factory = APIRequestFactory()

    request = factory.delete(f"/api/projects/{mock_project_orm.id}/")
    request.user = mock_user_orm["auth_admin"]

    view = ProjectViewSet.as_view({"delete": "destroy"})
    response = view(request, pk=str(mock_project_orm.id))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(mock_project_orm.id)
    assert response.data["deleted_at"].startswith("20")


@pytest.mark.django_db
def test_partial_update_project(
    mock_user_orm: dict,
    allow_any_permission: MagicMock,
    mock_project_orm: Project,
) -> None:
    """
    Project partial update test
    """
    factory = APIRequestFactory()

    new_data = {
        "name": "Project2",
    }

    request = factory.patch(
        f"/api/projects/{mock_project_orm.id}/",
        data=new_data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = ProjectViewSet.as_view({"patch": "partial_update"})
    response = view(request, pk=str(mock_project_orm.id))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == new_data["name"]


@pytest.mark.django_db
def test_update_project(
    mock_user_orm: dict,
    allow_any_permission: MagicMock,
    mock_project_orm: Project,
) -> None:
    """
    Project complete update test
    """
    factory = APIRequestFactory()

    new_data = {
        "name": "Project2",
        "status": ProjectStatus.ACTIVE,
    }

    request = factory.patch(
        f"/api/projects/{mock_project_orm.id}/",
        data=new_data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = ProjectViewSet.as_view({"patch": "partial_update"})
    response = view(request, pk=str(mock_project_orm.id))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == new_data["name"]
    assert response.data["status"] == ProjectStatus.ACTIVE
