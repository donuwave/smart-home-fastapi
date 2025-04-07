from api_v1.session.service import SessionService


async def get_session_service() -> SessionService:
    return SessionService()
