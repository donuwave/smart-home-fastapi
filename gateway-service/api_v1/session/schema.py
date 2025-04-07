from pydantic import BaseModel
from typing_extensions import Optional


class SessionResponse(BaseModel):
    id: int
    access_token: str
    refresh_token: str
    device_id: str


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
