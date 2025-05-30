from fastapi.params import Form
from pydantic import BaseModel, EmailStr


class RegistrationRequest(BaseModel):
    email: EmailStr = Form()
    password: str = Form()
    device_id: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_id: str

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    access_token: str

class AuthResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


class CreateToken(BaseModel):
    token_type: str
    token_data: dict
    expire_minutes: int
