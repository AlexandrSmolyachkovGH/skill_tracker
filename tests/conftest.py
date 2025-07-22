from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture
from rest_framework.permissions import AllowAny

from project.auth import (
    RemoteJWTAuthentication,
    RemoteJWTUser,
)
from projects.models import Project
from skills.models import Skill
from tasks.models import Task, TaskAttachment, TaskStatus
from users.models import User, UserProject


@pytest.fixture
def f_user() -> User:
    user = User.objects.create(
        id=uuid4(),
        name="Fake",
        email="fake@fake.fake",
    )
    return user


@pytest.fixture
def f_project(f_user) -> Project:
    project = Project.objects.create(
        name="Fake",
        owner=f_user,
    )
    return project


@pytest.fixture
def f_skill() -> Skill:
    skill = Skill.objects.create(
        name="Fake",
    )
    return skill


@pytest.fixture
def f_task(f_user, f_project) -> Task:
    task = Task.objects.create(
        title="Fake",
        assigned_to=f_user,
        project=f_project,
    )
    return task


@pytest.fixture
def auth_admin() -> RemoteJWTUser:
    mock_user = RemoteJWTUser({
        "user_id": str(uuid4()),
        "email": "test@example.com",
        "role": "admin",
        "is_active": True,
        "is_verified": True
    })
    return mock_user


@pytest.fixture
def allow_any_permission(
    mocker: MockerFixture,
) -> MagicMock:
    mock = mocker.patch("users.views.UserViewSet.get_permissions")
    mock.return_value = [AllowAny()]
    return mock


@pytest.fixture
def mock_auth_admin(
    mocker: MockerFixture,
    auth_admin: RemoteJWTUser,
) -> RemoteJWTUser:
    mocker.patch.object(
        RemoteJWTAuthentication,
        "authenticate",
        return_value=(auth_admin, "mock-token"),
    )
    return auth_admin


@pytest.fixture
def mock_user_orm(
    mocker: MockerFixture,
    mock_auth_admin: RemoteJWTUser,
    allow_any_permission: MagicMock,
) -> dict:
    user = User.objects.create(
        id=uuid4(),
        name="User",
        email="email@example.com",
    )
    user.refresh_from_db()
    mock_auth_admin.id = user.id
    mock_auth_admin.role = "USER"
    return {
        "user_orm": user,
        "auth_admin": mock_auth_admin,
    }


@pytest.fixture
def mock_project_orm(
    mock_user_orm: dict,
) -> Project:
    project = Project.objects.create(
        name="Project",
        owner=mock_user_orm["user_orm"],
    )
    UserProject.objects.create(
        user=mock_user_orm["user_orm"],
        project=project,
    )
    return project


@pytest.fixture
def mock_task(
    mock_project_orm: Project,
    mock_user_orm: dict,
) -> Task:
    create_data = {
        "title": "NewTask",
        "status": TaskStatus.NEW,
        "project": mock_project_orm,
        "assigned_to": mock_user_orm["user_orm"],
    }
    new_task = Task.objects.create(**create_data)
    return new_task


@pytest.fixture
def mock_attachment(
    mock_project_orm: Project,
    mock_user_orm: dict,
    mock_task: Task,
) -> TaskAttachment:
    new_attachment = TaskAttachment.objects.create(
        task=mock_task,
        file_url="test.url"
    )
    return new_attachment


@pytest.fixture
def allow_user_project_permission(
    mocker: MockerFixture,
) -> MagicMock:
    mock_permissions = mocker.patch(
        "users.views.UserProjectViewSet.get_permissions",
        return_value=[AllowAny()],
    )
    return mock_permissions
