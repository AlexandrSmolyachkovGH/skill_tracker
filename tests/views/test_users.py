from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
)

from project.auth import RemoteJWTUser
from users.models import User
from users.views import UserViewSet


@pytest.mark.django_db
def test_get_user_list(
    mock_auth_admin: RemoteJWTUser,
    allow_any_permission: MagicMock,
    f_user: User,
) -> None:
    """
    Test of receiving multiple user records
    """
    factory = APIRequestFactory()

    request = factory.get("/api/users/")
    request.user = mock_auth_admin

    view = UserViewSet.as_view({"get": "list"})
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["id"] == str(f_user.id)
    assert response.data["results"][0]["name"] == f_user.name


@pytest.mark.django_db
def test_get_user(
    mock_auth_admin: RemoteJWTUser,
    allow_any_permission: MagicMock,
    f_user: User,
) -> None:
    """
    Single user record receiving test
    """
    factory = APIRequestFactory()

    request = factory.get(f"/api/users/{f_user.id}/")
    request.user = mock_auth_admin

    view = UserViewSet.as_view({"get": "retrieve"})
    response = view(request, pk=f_user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(f_user.id)
    assert response.data["name"] == f_user.name


@pytest.mark.django_db
def test_create_user(
    mock_auth_admin: RemoteJWTUser,
    allow_any_permission: MagicMock,
) -> None:
    """
    User creation test
    """
    factory = APIRequestFactory()

    data = {
        "id": uuid4(),
        "name": "User1",
        "email": "user1@mail.com",
    }

    request = factory.post(
        "/api/users/",
        data=data,
        format="json",
    )
    view = UserViewSet.as_view({"post": "create"})
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == str(data["id"])
    assert response.data["name"] == data["name"]


@pytest.mark.django_db
def test_delete_user(
    mock_auth_admin: RemoteJWTUser,
    allow_any_permission: MagicMock,
    f_user: User,
) -> None:
    """
    User deletion test
    """
    factory = APIRequestFactory()

    request = factory.delete(f"/api/users/{f_user.id}/")
    request.user = mock_auth_admin

    view = UserViewSet.as_view({"delete": "destroy"})
    response = view(request, pk=str(f_user.id))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(f_user.id)
    assert isinstance(response.data["deleted_at"], str)
    assert response.data["deleted_at"].startswith("20")


@pytest.mark.django_db
def test_partial_update_user(
    mock_auth_admin: RemoteJWTUser,
    allow_any_permission: MagicMock,
    f_user: User,
) -> None:
    """
    User update test
    """
    factory = APIRequestFactory()

    new_data = {
        "name": "User2",
    }

    request = factory.patch(
        f"/api/users/{f_user.id}/",
        data=new_data,
        format="json",
    )
    mock_auth_admin.id = f_user.id
    request.user = mock_auth_admin

    view = UserViewSet.as_view({"patch": "partial_update"})
    response = view(request, pk=str(f_user.id))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == new_data["name"]
