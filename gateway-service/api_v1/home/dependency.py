from api_v1.home.service import HomeService


async def get_home_service() -> HomeService:
    return HomeService()