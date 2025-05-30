import pytest

from tasks.models import (
    Task,
    TaskAttachment,
    TaskStatus,
)


@pytest.mark.django_db
def test_task_model(f_user, f_project) -> None:
    task_model = Task.objects.create(
        title='TestTask',
        status=TaskStatus.NEW,
        assigned_to=f_user,
        project=f_project,
    )
    assert Task.objects.filter(
        title='TestTask',
    ).exists()
    assert task_model.title == 'TestTask'
    assert task_model.status == 'new'
    assert task_model.get_status_display() == 'Новая'
    task_model.delete()
    assert not Task.objects.filter(
        title='TestTask',
    ).exists()


@pytest.mark.django_db
def test_task_str_repr(f_user, f_project) -> None:
    tm = Task(
        title='TestTask',
        status=TaskStatus.NEW,
        assigned_to=f_user,
        project=f_project,
    )
    assert str(tm) == "Task: TestTask, status: new"


@pytest.mark.django_db
def test_task_attachment_model(f_task) -> None:
    ta_model = TaskAttachment.objects.create(
        task=f_task,
        file_url='https://test-task.test/'
    )
    assert TaskAttachment.objects.filter(
        task=f_task,
    ).exists()
    assert ta_model.file_url == 'https://test-task.test/'
    ta_model.delete()
    assert not TaskAttachment.objects.filter(
        task=f_task,
    ).exists()


@pytest.mark.django_db
def test_task_attachment_str_repr(f_task) -> None:
    tam = TaskAttachment(
        task=f_task,
        file_url='https://test-task.test/'
    )
    assert str(tam) == f"TaskID: {tam.task}, url: {tam.file_url}"
