from api_v1.device.service import DeviceService


async def get_device_service() -> DeviceService:
    return DeviceService()