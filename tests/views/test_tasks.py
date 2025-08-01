from unittest.mock import MagicMock

import pytest
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
)

from projects.models import (
    Project,
)
from tasks.models import (
    Task,
    TaskStatus,
)
from tasks.views import (
    TaskViewSet,
)


@pytest.mark.django_db
def test_get_task_list(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
) -> None:
    """
    Test of receiving multiple task records
    """
    factory = APIRequestFactory()

    request = factory.get(
        f"/api/projects/{mock_project_orm.id}/tasks/",
    )
    request.user = mock_user_orm["auth_admin"]

    view = TaskViewSet.as_view({"get": "list"})
    response = view(
        request,
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["title"] == mock_task.title


@pytest.mark.django_db
def test_get_task(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
) -> None:
    """
    Single task record receiving test
    """
    factory = APIRequestFactory()

    request = factory.get(
        f"/api/projects/{mock_project_orm.id}/tasks/{mock_task.id}",
    )
    request.user = mock_user_orm["auth_admin"]

    view = TaskViewSet.as_view({"get": "retrieve"})
    response = view(
        request,
        pk=str(mock_task.id),
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == mock_task.title


@pytest.mark.django_db
def test_create_task(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
) -> None:
    """
    Task creation test
    """
    factory = APIRequestFactory()

    data = {
        "title": "NewTask",
        "status": TaskStatus.NEW,
    }

    request = factory.post(
        f"/api/projects/{mock_project_orm.id}/tasks/",
        data=data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = TaskViewSet.as_view({"post": "create"})
    response = view(
        request,
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == data["title"]
    assert response.data["status"] == TaskStatus.NEW


@pytest.mark.django_db
def test_delete_task(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
) -> None:
    """
    Task deletion test
    """
    factory = APIRequestFactory()

    request = factory.delete(
        f"/api/projects/{mock_project_orm.id}/tasks/{mock_task.id}",
    )
    request.user = mock_user_orm["auth_admin"]

    view = TaskViewSet.as_view({"delete": "destroy"})
    response = view(
        request,
        pk=str(mock_task.id),
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["deleted_at"].startswith("20")


@pytest.mark.django_db
def test_partial_update_task(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
) -> None:
    """
    Task partial update test
    """
    factory = APIRequestFactory()

    new_data = {
        "title": "UpdatedTitle",
        "status": TaskStatus.IN_PROGRESS,
    }

    request = factory.patch(
        f"/api/projects/{mock_project_orm.id}/tasks/{mock_task.id}",
        data=new_data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = TaskViewSet.as_view({"patch": "partial_update"})
    response = view(
        request,
        pk=str(mock_task.id),
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == new_data["title"]
    assert response.data["status"] == TaskStatus.IN_PROGRESS


@pytest.mark.django_db
def test_get_all_tasks(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
) -> None:
    """
    Test of receiving all task records
    """
    factory = APIRequestFactory()

    request = factory.get(
        "/api/tasks/all-tasks/",
    )
    user = mock_user_orm["auth_admin"]
    if user.role == "USER":
        user.role = "ADMIN"
    request.user = user

    view = TaskViewSet.as_view({"get": "list"})
    response = view(
        request,
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
