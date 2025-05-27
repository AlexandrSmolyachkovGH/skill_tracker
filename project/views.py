from django.http import HttpRequest, JsonResponse


def api_root(
    request: HttpRequest,
) -> JsonResponse:  # pylint: disable=unused-argument
    return JsonResponse(
        {
            "title": "Skill Tracker REST API",
            "docs": "/api/schema/swagger-ui/",
            "redoc": "api/schema/redoc/",
            "version": "1.0.0",
        }
    )
