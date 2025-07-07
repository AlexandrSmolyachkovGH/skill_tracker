from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from project.views import api_root
from projects.views import router as project_router
from skills.views import router as skill_router
from tasks.views import router as task_router
from users.views import router as user_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", api_root),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # CRUDs:
    path("api/users/", include(user_router.urls)),
    path("api/skills/", include(skill_router.urls)),
    path("api/projects/", include(project_router.urls)),
    path("api/tasks/", include(task_router.urls)),
]
