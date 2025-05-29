import pytest

from projects.models import Project
from skills.models import Skill
from tasks.models import Task
from users.models import User


@pytest.fixture
def f_user():
    user = User.objects.create(
        name='Fake',
        email='fake@fake.fake',
    )
    return user


@pytest.fixture
def f_project(f_user):
    project = Project.objects.create(
        name='Fake',
        owner=f_user,
    )
    return project


@pytest.fixture
def f_skill():
    skill = Skill.objects.create(
        name='Fake',
    )
    return skill


@pytest.fixture
def f_task(f_user, f_project):
    skill = Task.objects.create(
        title='Fake',
        assigned_to=f_user.id,
        project=f_project.id,
    )
    return skill
