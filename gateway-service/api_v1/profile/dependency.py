from api_v1.profile.service import ProfileService


async def get_profile_service() -> ProfileService:
    return ProfileService()
