from pydantic import EmailStr

from api_v1.notifcation.dependency import get_notification_service
from api_v1.notifcation.schema import NotificationRequest, NotificationResponse
from config.database import db_helper


async def pick_service(key: str, body: dict | int | str | EmailStr) -> list | dict[str, dict]:
    service = key.split(".")[0]
    handler = key.split(".")[1]
    session = await db_helper.scoped_session_dependency()

    if service == "notification":
        notification_service = await get_notification_service(session=session)

        if handler == "send_push":
            await notification_service.send_push(notification_request=NotificationRequest(**body))

        if handler == "get_list_notification":
            notification_list = await notification_service.get_list_notification(home_id=body)
            return [
                NotificationResponse.model_validate(notification_item).model_dump()
                for notification_item in notification_list
            ]

    return dict()
