from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.permissions import AllowAny

from project.views import api_root
from projects.views import project_nested_router
from projects.views import router as project_router

# from skills.views import router as skill_router
from tasks.views import router as task_router
from tasks.views import task_nested_router
from users.views import router as user_router
from users.views import user_project_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api_root),
    # Optional UI:
    path(
        "api/schema/",
        SpectacularAPIView.as_view(
            authentication_classes=[],
            permission_classes=[AllowAny],
        ),
        name="schema",
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
            authentication_classes=[],
            permission_classes=[AllowAny],
        ),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
            authentication_classes=[],
            permission_classes=[AllowAny],
        ),
        name="redoc",
    ),
    # CRUDs:
    path("api/", include(user_router.urls)),
    path("api/", include(user_project_router.urls)),
    path("api/", include(project_router.urls)),
    path("api/", include(project_nested_router.urls)),
    path("api/", include(task_router.urls)),
    path("api/", include(task_nested_router.urls)),
    # path("api/skills/", include(skill_router.urls)),
]
