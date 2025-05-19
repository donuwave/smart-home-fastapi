from dataclasses import dataclass

from api_v1.device.repository import DeviceRepository
from api_v1.device.schema import GetDeviceResponse, CreateDeviceRequest


@dataclass
class DeviceService:
    device_repository: DeviceRepository

    async def get_list_device_in_home(self, home_id: int) -> list[GetDeviceResponse]:
        return await self.device_repository.get_list_device_in_home(home_id=home_id)

    async def get_item_device_in_home(self, device_id: int) -> GetDeviceResponse:
        return await self.device_repository.get_item_device_in_home(device_id=device_id)

    async def create_device(self, created_device: CreateDeviceRequest):
        return await self.device_repository.create_device(created_device=created_device)