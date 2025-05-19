from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.device.repository import DeviceRepository
from api_v1.device.service import DeviceService


async def get_device_repository(session: AsyncSession) -> DeviceRepository:
    return DeviceRepository(db_session=session)


async def get_device_service(session: AsyncSession) -> DeviceService:
    device_repository: DeviceRepository = await get_device_repository(session=session)
    return DeviceService(device_repository=device_repository)
