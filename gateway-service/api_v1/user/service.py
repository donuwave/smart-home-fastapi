from dataclasses import dataclass

from pydantic import EmailStr

from api_v1.user.schema import UserCreate


@dataclass
class UserService:
    async def get_user_by_id(self, user_id: int) -> UserCreate:
        pass

    async def get_user_by_email(self, email: EmailStr) -> UserCreate:
        pass

    async def create_user(self, user_create: UserCreate) -> int:
        pass
