from api_v1.profile.repository import ProfileRepository

async def get_profile_repository() -> ProfileRepository:
    return ProfileRepository()
