from dataclasses import dataclass

from fastapi import HTTPException
from firebase_admin import messaging

from api_v1.notifcation.schema import NotificationRequest


@dataclass
class FirebaseRepository:
    async def send_push(self, notification_request: NotificationRequest):
        message = messaging.Message(
            token=notification_request.token,
            notification=messaging.Notification(
                title=notification_request.title,
                body=notification_request.body,
            )
        )
        try:
            message_id = messaging.send(message)
            return {"success": True, "message_id": message_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))