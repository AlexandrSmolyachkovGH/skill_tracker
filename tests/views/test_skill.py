from unittest.mock import MagicMock

import pytest
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
)

from skills.models import SkillCategory
from skills.serializers import (
    UserSkillSerializer,
)
from skills.views import SkillViewSet


@pytest.mark.django_db
def test_get_skill_list(
    mock_user_orm: dict,
    skill_and_user_skill_mock: dict,
    allow_any_permission: MagicMock,
) -> None:
    """
    Test of receiving multiple Skill records
    """
    factory = APIRequestFactory()
    user_orm = mock_user_orm["user_orm"]

    request = factory.get(
        f"/api/users/{user_orm.id}/skills/",
    )
    request.user = mock_user_orm["auth_admin"]

    view = SkillViewSet.as_view({"get": "list"})
    response = view(
        request,
        users_pk=str(user_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_skill(
    mock_user_orm: dict,
    skill_and_user_skill_mock: dict,
    allow_any_permission: MagicMock,
) -> None:
    """
    Single skill record receiving test
    """
    factory = APIRequestFactory()
    user_orm = mock_user_orm["user_orm"]
    skill_orm, user_skill_orm = skill_and_user_skill_mock.values()
    serializer = UserSkillSerializer(user_skill_orm)

    request = factory.get(
        f"/api/users/{user_orm.id}/skills/{skill_orm.id}",
    )
    request.user = mock_user_orm["auth_admin"]

    view = SkillViewSet.as_view({"get": "retrieve"})
    response = view(
        request,
        users_pk=str(user_orm.id),
        pk=str(skill_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


@pytest.mark.django_db
def test_create_skill(
    mock_user_orm: dict,
    allow_any_permission: MagicMock,
) -> None:
    """
    Skill and UserSkill creation test
    """
    factory = APIRequestFactory()
    user_orm = mock_user_orm["user_orm"]
    data = {
        "name": "test_skill_title",
        "category": SkillCategory.UNSPECIFIED,
        "level": 3,
        "xp": 3,
    }

    request = factory.post(
        f"/api/users/{user_orm.id}/skills/",
        data=data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = SkillViewSet.as_view({"post": "create"})
    response = view(
        request,
        users_pk=str(user_orm.id),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["level"] == data["level"]


@pytest.mark.django_db
def test_partial_update_skill(
    mock_user_orm: dict,
    skill_and_user_skill_mock: dict,
    allow_any_permission: MagicMock,
) -> None:
    """
    Skill and UserSkill partial update test
    """
    factory = APIRequestFactory()
    user_orm = mock_user_orm["user_orm"]
    skill_orm, _ = skill_and_user_skill_mock.values()

    data = {
        "name": "test_skill_title",
        "category": SkillCategory.OTHER,
        "level": 3,
        "xp": 3,
    }

    request = factory.patch(
        f"/api/users/{user_orm.id}/skills/{skill_orm.id}",
        data=data,
        format="json",
    )
    request.user = mock_user_orm["auth_admin"]

    view = SkillViewSet.as_view({"patch": "partial_update"})
    response = view(
        request,
        users_pk=str(user_orm.id),
        pk=str(skill_orm.id),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["level"] == data["level"]


@pytest.mark.django_db
def test_delete_skill(
    mock_user_orm: dict,
    skill_and_user_skill_mock: dict,
    allow_any_permission: MagicMock,
) -> None:
    """
    Skill and UserSkill deletion test
    """
    factory = APIRequestFactory()
    user_orm = mock_user_orm["user_orm"]
    skill_orm, _ = skill_and_user_skill_mock.values()

    request = factory.delete(
        f"/api/users/{user_orm.id}/skills/{skill_orm.id}",
    )
    request.user = mock_user_orm["auth_admin"]

    view = SkillViewSet.as_view({"delete": "destroy"})
    response = view(
        request,
        users_pk=str(user_orm.id),
        pk=str(skill_orm.id),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data["deleted_at"] != str(skill_orm.deleted_at)
    assert response.data["id"] == str(skill_orm.id)
