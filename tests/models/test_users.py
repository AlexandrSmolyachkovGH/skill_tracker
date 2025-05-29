import pytest

from users.models import (
    User,
    UserProject,
    UserProjectRole,
    UserSkill,
)


@pytest.mark.django_db
def test_create_user_model() -> None:
    user_model = User.objects.create(
        name='TestName',
        email='test@test.test',
    )
    assert user_model.name == 'TestName'
    assert user_model.email == 'test@test.test'


@pytest.mark.django_db
def test_user_str_repr() -> None:
    user_model = User.objects.create(
        name='TestName',
        email='test@test.test',
    )
    assert str(user_model) == "User: TestName, email: test@test.test"


@pytest.mark.django_db
def test_create_user_project_model(f_user, f_project) -> None:
    user_project_model = UserProject.objects.create(
        user=f_user,
        project=f_project,
        role=UserProjectRole.CREATOR,
    )
    assert user_project_model.role == 'creator'


@pytest.mark.django_db
def test_user_project_str_repr(f_user, f_project) -> None:
    user_project_model = UserProject.objects.create(
        user=f_user,
        project=f_project,
        role=UserProjectRole.CREATOR,
    )
    assert str(user_project_model) == f"user: {f_user}, project: {f_project}, role: creator"
