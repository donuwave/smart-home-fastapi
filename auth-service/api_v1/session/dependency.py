from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.session.repository import SessionRepository
from api_v1.session.service import SessionService


async def get_session_repository(session: AsyncSession) -> SessionRepository:
    return SessionRepository(db_session=session)


async def get_session_service(session: AsyncSession) -> SessionService:
    session_repository: SessionRepository = await get_session_repository(session=session)
    return SessionService(session_repository=session_repository)
