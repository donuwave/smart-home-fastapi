from dataclasses import dataclass

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user import User
from api_v1.user.schema import UserCreate


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, user_create: UserCreate) -> int:
        user = User(**user_create.model_dump())
        self.db_session.add(user)
        await self.db_session.commit()
        return user.id

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        user = await self.db_session.execute(query)
        return user.scalar()

    async def get_user_by_email(self, email: EmailStr) -> User:
        query = select(User).where(User.email == email)
        user = await self.db_session.execute(query)
        return user.scalar()
