from dataclasses import dataclass

from fastapi import Response, status
from fastapi.security import HTTPAuthorizationCredentials

from api_v1.auth.schema import RegistrationRequest, AuthResponse, LoginRequest
from config.broker import connection_broker


@dataclass
class AuthService:
    queue_name = "auth_queue"
    queue_name_callback = "callback_auth_queue"

    async def login(self, login_request: LoginRequest) -> AuthResponse:
        body = {
            "key": "auth.login",
            "body": dict(login_request)
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def registration(self, register_request: RegistrationRequest) -> AuthResponse:
        body = {
            "key": "auth.registration",
            "body": dict(register_request)
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def refresh(self, credentials: HTTPAuthorizationCredentials) -> AuthResponse:
        body = {
            "key": "auth.refresh",
            "body": {
                "refresh_token": credentials.credentials
            }
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def logout(self, credentials: HTTPAuthorizationCredentials, response: Response):
        body = {
            "key": "auth.logout",
            "body": {
                "access_token": credentials.credentials
            }
        }

        logout_response = await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

        if logout_response is None:
            response.status_code = status.HTTP_200_OK

        return logout_response