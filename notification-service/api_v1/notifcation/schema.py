from pydantic import BaseModel


class NotificationRequest(BaseModel):
    token: str
    title: str
    home_id: int
    body: str

class NotificationResponse(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        from_attributes = True