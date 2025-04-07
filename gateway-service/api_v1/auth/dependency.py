from api_v1.auth.service import AuthService


async def get_auth_service() -> AuthService:
    return AuthService()