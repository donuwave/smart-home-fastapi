from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ProfileBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[int] = Field(
        None, description="Пол: 1 - мужской, 2 - женский", ge=1, le=2
    )


class ProfileCreateRequest(ProfileBase):
    model_config = ConfigDict(from_attributes=True)


class ProfileGetResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
