import json
from dataclasses import dataclass
from fastapi.security import HTTPAuthorizationCredentials

from api_v1.auth.schema import RegistrationRequest, AuthResponse, LoginRequest
from config.broker import connection_broker


@dataclass
class AuthService:
    async def login(self, login_request: LoginRequest) -> AuthResponse:
        body = {
            "key": "auth.login",
            "body": dict(login_request)
        }

        return await connection_broker(queue_name="auth_queue", queue_name_callback="callback_auth_queue", body=body)

    async def registration(self, register_request: RegistrationRequest) -> AuthResponse:
        body = {
            "key": "auth.registration",
            "body": dict(register_request)
        }

        return await connection_broker(queue_name="auth_queue", queue_name_callback="callback_auth_queue", body=body)

    async def refresh(self, credentials: HTTPAuthorizationCredentials) -> AuthResponse:
        pass

    async def logout(self, credentials: HTTPAuthorizationCredentials):
        pass
