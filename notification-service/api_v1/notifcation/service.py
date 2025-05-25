from dataclasses import dataclass

from api_v1.notifcation.model import NotificationRequest
from api_v1.notifcation.repository import NotificationRepository


@dataclass
class NotificationService:
    notification_repository: NotificationRepository

    async def send_push(self, notification_request: NotificationRequest):
        return await self.notification_repository.send_push(notification_request=notification_request)