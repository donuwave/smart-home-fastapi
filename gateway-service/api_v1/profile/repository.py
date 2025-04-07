from dataclasses import dataclass
from typing import Optional
from api_v1.profile.schema import ProfileCreateRequest, ProfileGetResponse


@dataclass
class ProfileRepository:

    async def get_profile_by_id(self, profile_id: int) -> Optional[ProfileGetResponse]:
        pass

    async def create_profile(self, profile_create: ProfileCreateRequest) -> int:
        pass
