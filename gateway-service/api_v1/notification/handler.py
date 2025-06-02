from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from typing import Annotated

from api_v1.notification.dependency import get_notification_service
from api_v1.notification.schema import PushParams
from api_v1.notification.service import NotificationService

router = APIRouter(tags=["notification"])
http_bearer = HTTPBearer()

@router.post("/push")
async def send_push(
    push_params: PushParams,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)]
):
    return await notification_service.send_push(push_params=push_params)


@router.get("/{home_id}")
async def get_list_notification_by_id(
    home_id: int,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)]
):
    return await notification_service.get_list_notification(home_id=home_id)