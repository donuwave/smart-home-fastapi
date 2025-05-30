from pydantic import BaseModel, EmailStr


class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    device_id: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_id: str


class AuthResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


class CreateToken(BaseModel):
    token_type: str
    token_data: dict
    expire_minutes: int
