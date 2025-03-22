from api_v1.profile.repository import ProfileRepository
from api_v1.profile.schema import ProfileCreateRequest


class ProfileService:
    profile_repository: ProfileRepository

    async def create_profile(self, profile: ProfileCreateRequest):
        return await self.profile_repository.create_profile(profile)
