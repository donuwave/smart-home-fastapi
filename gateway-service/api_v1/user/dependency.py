from api_v1.user.service import UserService


async def get_user_service(
) -> UserService:
    return UserService()
