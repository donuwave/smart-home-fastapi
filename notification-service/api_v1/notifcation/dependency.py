from api_v1.notifcation.repository import NotificationRepository
from api_v1.notifcation.service import NotificationService


async def get_notification_repository() -> NotificationRepository:
    return NotificationRepository()

async def get_notification_service() -> NotificationService:
    notification_repository: NotificationRepository = await get_notification_repository()
    return NotificationService(notification_repository=notification_repository)