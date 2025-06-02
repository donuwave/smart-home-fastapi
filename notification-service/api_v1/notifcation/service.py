from dataclasses import dataclass

from api_v1.firebase.repository import FirebaseRepository
from api_v1.notifcation.schema import NotificationRequest, NotificationResponse
from api_v1.notifcation.repository import NotificationRepository


@dataclass
class NotificationService:
    firebase_repository: FirebaseRepository
    notification_repository: NotificationRepository

    async def send_push(self, notification_request: NotificationRequest):
        await self.notification_repository.create_device(title=notification_request.title, body=notification_request.body, home_id=notification_request.home_id)
        return await self.firebase_repository.send_push(notification_request=notification_request)

    async def get_list_notification(self, home_id: int) -> list[NotificationResponse]:
        return await self.notification_repository.get_list_notification_in_home(home_id=home_id)