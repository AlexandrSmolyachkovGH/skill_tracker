import os

from celery import Celery

os.environ.setdefault(
    key="DJANGO_SETTINGS_MODULE",
    value="project.settings",
)

celery_app = Celery(
    main="skill_core_celery",
)

celery_app.config_from_object(
    obj="django.conf:settings",
    namespace="CELERY",
)

celery_app.autodiscover_tasks()
