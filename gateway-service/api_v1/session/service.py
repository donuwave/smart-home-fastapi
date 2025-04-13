from dataclasses import dataclass

from config.broker import connection_broker


@dataclass
class SessionService:

    async def get_session(self, session_id: int):
        body = {
            "key": "session.get_session",
            "body": session_id
        }

        return await connection_broker(queue_name="auth_queue", queue_name_callback="callback_auth_queue", body=body)