from api_v1.notification.service import NotificationService


async def get_notification_service() -> NotificationService:
    return NotificationService()