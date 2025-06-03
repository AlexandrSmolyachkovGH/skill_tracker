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
        username='TestName',
        email='test@test.test',
    )
    assert user_model.username == 'TestName'
    assert user_model.email == 'test@test.test'
    assert User.objects.filter(
        id=user_model.id
    ).exists()
    user_model.delete()
    assert not User.objects.filter(
        id=user_model.id
    ).exists()


def test_user_str_repr() -> None:
    user_model = User(
        username='TestName',
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
    assert user_project_model.get_role_display() == 'Владелец'
    assert UserProject.objects.filter(
        user=f_user,
        project=f_project,
    ).count() == 1
    user_project_model.delete()
    assert UserProject.objects.filter(
        user=f_user,
        project=f_project,
    ).count() == 0


@pytest.mark.django_db
def test_user_project_str_repr(f_user, f_project) -> None:
    user_project_model = UserProject(
        user=f_user,
        project=f_project,
        role=UserProjectRole.CREATOR,
    )
    assert str(user_project_model) == f"user: {f_user}, project: {f_project}, role: creator"


@pytest.mark.django_db
def test_user_skill_model(f_user, f_skill):
    user_skill_model = UserSkill.objects.create(
        user=f_user,
        skill=f_skill,
    )
    assert user_skill_model.level == 1
    assert user_skill_model.xp == 0
    assert UserSkill.objects.filter(
        user=f_user,
        skill=f_skill,
    ).exists()
    user_skill_model.delete()
    assert not UserSkill.objects.filter(
        user=f_user,
        skill=f_skill,
    ).exists()


@pytest.mark.django_db
def test_user_skill_str_repr(f_user, f_skill):
    usm = UserSkill(
        user=f_user,
        skill=f_skill,
    )
    assert str(usm) == (
        f"user: {usm.user}, skill: {usm.skill},"
        f"level: {usm.level}, xp: {usm.xp}"
    )
