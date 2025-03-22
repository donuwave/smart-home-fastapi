from dataclasses import dataclass

from pydantic import EmailStr

from api_v1.user import User
from api_v1.user.repository import UserRepository
from api_v1.user.schema import UserCreate


@dataclass
class UserService:
    user_repository: UserRepository

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: EmailStr) -> User:
        return await self.user_repository.get_user_by_email(email=email)

    async def create_user(self, user_create: UserCreate) -> int:
        return await self.user_repository.create_user(user_create=user_create)
