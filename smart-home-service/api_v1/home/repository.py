from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.home import Home
from api_v1.home.schema import HomeCreateRequest, GetHomeResponse, AddDeviceRequest


@dataclass
class HomeRepository:
    db_session: AsyncSession

    async def get_home_list(self) -> list[GetHomeResponse]:
        result = await self.db_session.execute(select(Home))
        return result.scalars().all()

    async def get_home_by_id(self, home_id: int) -> Optional[GetHomeResponse]:
        result = await self.db_session.execute(select(Home).where(Home.id == home_id))
        return result.scalar()

    async def get_home_list_by_user_id(self, user_id: int) -> list[GetHomeResponse]:
        result =  await self.db_session.execute(select(Home).where(Home.owner_id == user_id))
        return result.scalars().all()

    async def create_home(self, created_home: HomeCreateRequest):
        home = Home(**created_home.model_dump())
        self.db_session.add(home)
        await self.db_session.commit()

    async def add_device_in_home(self, added_device: AddDeviceRequest):
        pass