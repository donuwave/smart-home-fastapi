from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: bytes
    profile_id: int

class User(BaseModel):
    email: EmailStr
    password: bytes
    profile_id: int

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    email: EmailStr
    profile_id: int