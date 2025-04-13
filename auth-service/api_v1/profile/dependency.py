from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profile.repository import ProfileRepository
from api_v1.profile.service import ProfileService


async def get_profile_repository(session: AsyncSession) -> ProfileRepository:
    return ProfileRepository(db_session=session)

async def get_profile_service(session: AsyncSession) -> ProfileService:
    profile_repository: ProfileRepository = await get_profile_repository(session=session)
    return ProfileService(profile_repository=profile_repository)