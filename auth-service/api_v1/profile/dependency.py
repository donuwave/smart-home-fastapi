from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profile.repository import ProfileRepository
from config.database import db_helper


async def get_profile_repository(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ProfileRepository:
    return ProfileRepository(db_session=session)
