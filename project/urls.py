from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from project.views import api_root

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
]  # ___
