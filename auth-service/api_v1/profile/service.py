from api_v1.profile.repository import ProfileRepository
from api_v1.profile.schema import ProfileCreateRequest, ProfileGetResponse
from dataclasses import dataclass

@dataclass
class ProfileService:
    profile_repository: ProfileRepository

    async def create_profile(self, profile: ProfileCreateRequest):
        return await self.profile_repository.create_profile(profile_create=profile)

    async def get_profile_by_id(self, profile_id: int) -> ProfileGetResponse:
        return await self.profile_repository.get_profile_by_id(profile_id=profile_id)
