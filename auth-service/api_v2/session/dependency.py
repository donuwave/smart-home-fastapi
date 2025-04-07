from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.session.repository import SessionRepository
from api_v1.session.service import SessionService
from config.database import db_helper


async def get_session_repository(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> SessionRepository:
    return SessionRepository(db_session=session)


async def get_session_service(
    session_repository: SessionRepository = Depends(get_session_repository),
) -> SessionService:
    return SessionService(session_repository=session_repository)
