from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.notifcation import Notification
from api_v1.notifcation.schema import NotificationResponse


@dataclass
class NotificationRepository:
    db_session: AsyncSession

    async def get_list_notification_in_home(self, home_id: int) -> list[NotificationResponse]:
        result = await self.db_session.execute(select(Notification).where(Notification.home_id == home_id))
        return result.scalars().all()

    async def create_device(self, title: str, body: str, home_id: int):
        result = Notification(title=title, body=body, home_id=home_id)
        self.db_session.add(result)
        await self.db_session.commit()