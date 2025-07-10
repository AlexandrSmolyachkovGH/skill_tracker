from typing import Any

import requests
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from project.settings import (
    AUTH_URI,
)


class RemoteJWTUser(AnonymousUser):
    def __init__(
        self,
        payload: dict,
    ) -> None:
        super().__init__()
        self.id = payload.get("user_id")
        self.email = payload.get("email")
        self.role = payload.get("role")
        self.is_active = payload.get("is_active", True)
        self.is_verified = payload.get("is_verified", True)

    def get_username(self) -> str:
        return self.email or "remote-user"

    @property
    def is_authenticated(self) -> bool:
        return True

    def check_password(self, raw_password: str) -> bool:
        return False

    def set_password(self, raw_password: str) -> None:
        pass

    def save(self, *args: Any, **kwargs: Any) -> None:
        pass

    def delete(self, *args: Any, **kwargs: Any) -> None:
        pass


class RemoteJWTAuthentication(BaseAuthentication):
    auth_uri = f"{AUTH_URI}/tokens/access/verify/"

    def verify_token(
        self,
        token: str
    ) -> dict[str, Any]:
        """
        Extracts the token and verifies it on the Auth service side
        """
        cached = cache.get(f"token:{token[:200]}")
        if cached:
            return cached
        response = requests.get(
            self.auth_uri,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        if response.status_code != 200:
            raise AuthenticationFailed(
                f"Invalid token. Auth responded: {response.status_code} {response.text}"
            )
        payload = response.json()
        cache.set(f"token:{token[:200]}", payload, timeout=60)
        return payload

    def authenticate(
        self,
        request: Request,
        **kwargs: Any,
    ) -> tuple[RemoteJWTUser, str] | None:
        """
        Custom User authorization
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]

        try:
            token_data = self.verify_token(token=token)
        except requests.RequestException as exc:
            raise AuthenticationFailed("Auth service doesn't respond") from exc

        payload = token_data.get("payload")
        if not isinstance(payload, dict):
            raise AuthenticationFailed("Invalid payload format")

        user = RemoteJWTUser(payload)
        return user, token


class NoAuth(BaseAuthentication):
    def authenticate(
        self,
        request: Request,
    ) -> None:
        return None
