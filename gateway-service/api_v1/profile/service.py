from api_v1.profile.schema import ProfileCreateRequest
from dataclasses import dataclass

from config.broker import connection_broker

@dataclass
class ProfileService:
    async def get_profile_by_id(self, profile_id: int):
        body = {
            "key": "profile.get_profile_by_id",
            "body": profile_id
        }

        return await connection_broker(queue_name="auth_queue", queue_name_callback="callback_auth_queue", body=body)
