from dataclasses import dataclass
from sqlalchemy import select
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.device import Device
from api_v1.device.schema import GetDeviceResponse, CreateDeviceRequest


@dataclass
class DeviceRepository:
    db_session: AsyncSession

    async def get_all_device(self) -> list[GetDeviceResponse]:
        result = await self.db_session.execute(select(Device))
        return result.scalars().all()

    async def get_list_device_in_home(self, home_id: int) -> list[GetDeviceResponse]:
        result = await self.db_session.execute(select(Device).where(Device.home_id == home_id))
        return result.scalars().all()

    async def get_item_device_in_home(self, device_id: int) -> Optional[GetDeviceResponse]:
        result = await self.db_session.execute(select(Device).where(Device.id == device_id))
        return result.scalar()

    async def create_device(self, created_device: CreateDeviceRequest):
        result = Device(**created_device.model_dump())
        self.db_session.add(result)
        await self.db_session.commit()