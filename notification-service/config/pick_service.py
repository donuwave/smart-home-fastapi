from pydantic import EmailStr

from api_v1.notifcation.dependency import get_notification_service
from api_v1.notifcation.model import NotificationRequest


async def pick_service(key: str, body: dict | int | str | EmailStr) -> list | dict[str, dict]:
    service = key.split(".")[0]
    handler = key.split(".")[1]

    if service == "notification":
        notification_service = await get_notification_service()

        if handler == "send_push":
            await notification_service.send_push(notification_request=NotificationRequest(**body))

    return dict()
