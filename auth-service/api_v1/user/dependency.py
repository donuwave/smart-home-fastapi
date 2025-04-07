from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.repository import UserRepository
from api_v1.user.service import UserService
from config.database import db_helper


async def get_user_repository(session: AsyncSession) -> UserRepository:
    return UserRepository(db_session=session)

async def get_user_service() -> UserService:
    user_repository: UserRepository = await get_user_repository()
    return UserService(user_repository=user_repository)
