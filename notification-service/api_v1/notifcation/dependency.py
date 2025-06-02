from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.firebase.dependency import get_firebase_repository
from api_v1.firebase.repository import FirebaseRepository
from api_v1.notifcation.repository import NotificationRepository
from api_v1.notifcation.service import NotificationService


async def get_notification_repository(session: AsyncSession) -> NotificationRepository:
    return NotificationRepository(db_session=session)

async def get_notification_service(session: AsyncSession) -> NotificationService:
    notification_repository: NotificationRepository = await get_notification_repository(session=session)
    firebase_repository: FirebaseRepository = await get_firebase_repository()
    return NotificationService(notification_repository=notification_repository, firebase_repository=firebase_repository)