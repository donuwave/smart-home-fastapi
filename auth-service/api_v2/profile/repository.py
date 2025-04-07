from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profile import Profile
from api_v1.profile.schema import ProfileCreateRequest, ProfileGetResponse


@dataclass
class ProfileRepository:
    db_session: AsyncSession

    async def get_profile_by_id(self, profile_id: int) -> Optional[ProfileGetResponse]:
        query = select(Profile).where(Profile.id == profile_id)
        profile = await self.db_session.execute(query)
        return profile.scalar()

    async def create_profile(self, profile_create: ProfileCreateRequest) -> int:
        profile = Profile(**profile_create.model_dump())
        self.db_session.add(profile)
        await self.db_session.commit()
        return profile.id
