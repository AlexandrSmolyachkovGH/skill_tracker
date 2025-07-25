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
    TaskAttachment,
)
from tasks.views import (
    TaskAttachmentViewSet,
)


@pytest.mark.django_db
def test_get_attachment_list(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
    mock_attachment: TaskAttachment,
) -> None:
    """
    Test of receiving multiple TaskAttachment records
    """
    factory = APIRequestFactory()

    uri = (
        f"/api/projects/{mock_project_orm.id}"
        + f"/tasks/{mock_task.id}/attachments/",
    )
    request = factory.get(uri)
    request.user = mock_user_orm["auth_admin"]

    view = TaskAttachmentViewSet.as_view({"get": "list"})
    response = view(
        request,
        projects_pk=str(mock_project_orm.id),
        tasks_pk=str(mock_task.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["file_url"] == mock_attachment.file_url


@pytest.mark.django_db
def test_get_attachment(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
    mock_attachment: TaskAttachment,
) -> None:
    """
    Single TaskAttachment record receiving test
    """
    factory = APIRequestFactory()

    uri = (
        f"/api/projects/{mock_project_orm.id}"
        + f"/tasks/{mock_task.id}/attachments/{mock_attachment.id}/",
    )
    request = factory.get(uri)
    request.user = mock_user_orm["auth_admin"]

    view = TaskAttachmentViewSet.as_view({"get": "retrieve"})
    response = view(
        request,
        pk=str(mock_attachment.id),
        tasks_pk=str(mock_task.id),
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["file_url"] == mock_attachment.file_url


@pytest.mark.django_db
def test_create_attachment(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
) -> None:
    """
    TaskAttachment creation test
    """
    factory = APIRequestFactory()

    uri = (
        f"/api/projects/{mock_project_orm.id}"
        + f"/tasks/{mock_task.id}/attachments/",
    )
    data = {
        "task": str(mock_task.id),
        "file_url": "test.url",
    }
    request = factory.post(
        uri,
        data=data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = TaskAttachmentViewSet.as_view({"post": "create"})
    response = view(
        request,
        tasks_pk=str(mock_task.id),
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["task"] == mock_task.id
    assert response.data["file_url"] == data["file_url"]


@pytest.mark.django_db
def test_delete_attachment(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
    mock_attachment: TaskAttachment,
) -> None:
    """
    TaskAttachment deletion test
    """
    factory = APIRequestFactory()

    uri = (
        f"/api/projects/{mock_project_orm.id}"
        + f"/tasks/{mock_task.id}/attachments/{mock_attachment.id}/",
    )
    request = factory.delete(uri)
    request.user = mock_user_orm["auth_admin"]

    view = TaskAttachmentViewSet.as_view({"delete": "destroy"})
    response = view(
        request,
        pk=str(mock_attachment.id),
        tasks_pk=str(mock_task.id),
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_partial_update_attachment(
    mock_user_orm: dict,
    mock_project_orm: Project,
    allow_any_permission: MagicMock,
    mock_task: Task,
    mock_attachment: TaskAttachment,
) -> None:
    """
    TaskAttachment partial update test
    """
    factory = APIRequestFactory()

    new_data = {
        "file_url": "new_example.url",
    }
    uri = (
        f"/api/projects/{mock_project_orm.id}"
        + f"/tasks/{mock_task.id}/attachments/{mock_attachment.id}/",
    )
    request = factory.patch(
        path=uri,
        data=new_data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = TaskAttachmentViewSet.as_view({"patch": "partial_update"})
    response = view(
        request,
        pk=str(mock_attachment.id),
        tasks_pk=str(mock_task.id),
        projects_pk=str(mock_project_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["file_url"] == new_data["file_url"]
