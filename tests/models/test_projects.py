import pytest

from projects.models import (
    Project,
    ProjectStatus,
)


@pytest.mark.django_db
def test_project_model(f_user) -> None:
    project_model = Project.objects.create(
        name='TestProject',
        status=ProjectStatus.ACTIVE,
        owner=f_user,
    )
    assert project_model.name == 'TestProject'
    assert project_model.status == 'active'
    assert project_model.get_status_display() == 'Активный'
    assert Project.objects.filter(
        name='TestProject',
        status=ProjectStatus.ACTIVE,
        owner=f_user,
    ).exists()
    project_model.delete()
    assert not Project.objects.filter(
        name='TestProject',
        status=ProjectStatus.ACTIVE,
        owner=f_user,
    ).exists()


@pytest.mark.django_db
def test_project_str_repr(f_user) -> None:
    pm = Project(
        name='TestName',
        owner=f_user,
    )
    assert str(pm) == "Project: TestName, status: draft"
