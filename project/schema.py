from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema


class RemoteJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'project.auth.RemoteJWTAuthentication'
    name = 'RemoteJWTAuth'

    def get_security_definition(
        self,
        auto_schema: AutoSchema,
    ) -> dict:
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
