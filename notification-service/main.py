from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = FastAPI(title="Notification Service")

class NotificationRequest(BaseModel):
    token: str
    title: str
    body: str

@app.post("/send")
async def send_notification(req: NotificationRequest):
    message = messaging.Message(
        token=req.token,
        notification=messaging.Notification(
            title=req.title,
            body=req.body,
        )
    )
    try:
        message_id = messaging.send(message)
        return {"success": True, "message_id": message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
