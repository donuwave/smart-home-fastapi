from dataclasses import dataclass

from api_v1.home.schema import HomeCreateRequest
from config.broker import connection_broker


@dataclass
class HomeService:
    queue_name = "home_queue"
    queue_name_callback = "callback_home_queue"

    async def get_home_list(self):
        body = {
            "key": "home.get_home_list",
            "body": None
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def get_home_by_id(self, home_id: int):
        body = {
            "key": "home.get_home_by_id",
            "body": home_id
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def get_home_list_by_user_id(self, user_id: int):
        body = {
            "key": "home.get_home_list_by_user_id",
            "body": user_id
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def create_home(self, created_home: HomeCreateRequest):
        body = {
            "key": "home.create_home",
            "body": created_home
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)