from dataclasses import dataclass

from fastapi.security import HTTPAuthorizationCredentials

from api_v1.session.schema import SessionResponse
from config.broker import connection_broker


@dataclass
class SessionService:

    async def get_session(self, session_id: int) -> SessionResponse:
        body = {
            "key": "session.get_session",
            "body": session_id
        }

        return await connection_broker(queue_name="auth_queue", queue_name_callback="callback_auth_queue", body=body)


    async def get_list_session(self, credentials: HTTPAuthorizationCredentials) -> list[SessionResponse]:
        body = {
            "key": "session.get_list_session",
            "body": credentials.credentials
        }

        return await connection_broker(queue_name="auth_queue", queue_name_callback="callback_auth_queue", body=body)

    async def patch_session_fcm_token(self, credentials: HTTPAuthorizationCredentials, fcm_token: str):
        body = {
            "key": "session.patch_session_fcm_token",
            "body": {
                "access_token": credentials.credentials,
                "fcm_token": fcm_token
            }
        }

        await connection_broker(queue_name="auth_queue", queue_name_callback="callback_auth_queue", body=body)