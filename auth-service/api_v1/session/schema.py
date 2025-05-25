from pydantic import BaseModel
from typing_extensions import Optional


class SessionResponse(BaseModel):
    id: int
    access_token: str
    refresh_token: str
    device_id: str
    fcm_token: Optional[str] = None
    home_id: Optional[int] = None

    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    access_token: str
    refresh_token: str
    device_id: str
    user_id: int


class SessionUpdate(BaseModel):
    session_id: int
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    device_id: Optional[str] = None

class SessionByAccessToken(SessionResponse):
    user_id: int

class SessionUpdateHomeIdParams(BaseModel):
    access_token: str
    home_id: int

class SessionUpdateFCMTokenParams(BaseModel):
    access_token: str
    fcm_token: str