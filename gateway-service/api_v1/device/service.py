from dataclasses import dataclass

from api_v1.device.schema import CreateDeviceRequest
from config.broker import connection_broker


@dataclass
class DeviceService:
    queue_name = "home_queue"
    queue_name_callback = "callback_home_queue"

    async def get_list_device_in_home(self, home_id: int):
        body = {
            "key": "device.get_list_device_in_home",
            "body": home_id
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def get_item_device_in_home(self, device_id: int):
        body = {
            "key": "device.get_item_device_in_home",
            "body": device_id
        }

        return await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)

    async def create_device(self, created_device: CreateDeviceRequest):
        body = {
            "key": "device.create_device",
            "body": dict(created_device)
        }

        await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)
