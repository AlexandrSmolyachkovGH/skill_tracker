import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

# from users.models import User


class RemoteJWTAuthentication(BaseAuthentication):
    def authenticate(
        self,
        request: Request
    ) -> None:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            response = requests.get(
                'http://...',  # Заглушка
                headers={'Authorization': f'Bearer {token}'},
                timeout=5,
            )
        except requests.RequestException as exc:
            raise AuthenticationFailed("Auth service doesn't respond") from exc
        if response.status_code != 200:
            raise AuthenticationFailed("Invalid token")
        return None
