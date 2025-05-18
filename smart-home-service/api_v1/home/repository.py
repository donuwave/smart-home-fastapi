from dataclasses import dataclass

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.home import Home


@dataclass
class HomeRepository:
    db_session: AsyncSession

    async def get_home_list(self):
        result = await self.db_session.execute(select(Home))
        return result.scalars().all()

    async def get_home_by_id(self, home_id: int):
        result = await self.db_session.execute(select(Home).where(Home.id == home_id))
        return result.scalar()

    async def get_home_list_by_user_id(self, user_id):
        result =  await self.db_session.execute(select(Home))
        return result.scalars().all()