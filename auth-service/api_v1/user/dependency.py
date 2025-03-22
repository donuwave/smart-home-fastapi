from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.repository import UserRepository
from api_v1.user.service import UserService
from config.database import db_helper


async def get_user_repository(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserRepository:
    return UserRepository(db_session=session)


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=user_repository)
