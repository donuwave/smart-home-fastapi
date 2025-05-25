from dataclasses import dataclass

from fastapi.security import HTTPAuthorizationCredentials

from api_v1.session.schema import SessionResponse
from config.broker import connection_broker


@dataclass
class SessionService:
    queue_name = "auth_queue"
    queue_name_callback = "callback_auth_queue"

    async def get_session(self, session_id: int) -> SessionResponse:
        body = {
            "key": "session.get_session",
            "body": session_id
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def get_session_by_access_token(self, credentials: HTTPAuthorizationCredentials) -> SessionResponse:
        body = {
            "key": "session.get_session_by_access_token",
            "body": credentials.credentials
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)


    async def get_session_list_by_home_id(self, home_id: int) -> list[SessionResponse]:
        body = {
            "key": "session.get_list_session_by_home_id",
            "body": home_id
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)


    async def get_list_session(self, credentials: HTTPAuthorizationCredentials) -> list[SessionResponse]:
        body = {
            "key": "session.get_list_session",
            "body": credentials.credentials
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def patch_session_home_id(self, credentials: HTTPAuthorizationCredentials, home_id: int):
        body = {
            "key": "session.patch_session_home_id",
            "body": {
                "access_token": credentials.credentials,
                "home_id": home_id
            }
        }

        await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def patch_session_fcm_token(self, credentials: HTTPAuthorizationCredentials, fcm_token: str):
        body = {
            "key": "session.patch_session_fcm_token",
            "body": {
                "access_token": credentials.credentials,
                "fcm_token": fcm_token
            }
        }

        await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)