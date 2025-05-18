from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.home.repository import HomeRepository
from api_v1.home.service import HomeService


async def get_home_repository(session: AsyncSession) -> HomeRepository:
    return HomeRepository(db_session=session)


async def get_home_service(session: AsyncSession) -> HomeService:
    home_repository: HomeRepository = await get_home_repository(session=session)
    return HomeService(home_repository=home_repository)
