from dataclasses import dataclass

from api_v1.notification.schema import PushParams
from config.broker import connection_broker


@dataclass
class NotificationService:
    queue_name = "notification_queue"
    queue_name_callback = "callback_notification_queue"

    async def send_push(self, push_params: PushParams):
        body = {
            "key": "notification.send_push",
            "body": dict(push_params)
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)