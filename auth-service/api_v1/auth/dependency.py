from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.service import AuthService
from api_v1.profile.dependency import get_profile_repository
from api_v1.profile.repository import ProfileRepository
from api_v1.session.dependency import get_session_repository
from api_v1.session.repository import SessionRepository
from api_v1.user.dependency import get_user_repository
from api_v1.user.repository import UserRepository


async def get_auth_service(
    session: AsyncSession
) -> AuthService:
    user_repository: UserRepository = await get_user_repository(session=session)
    profile_repository: ProfileRepository = await get_profile_repository(session=session)
    session_repository: SessionRepository = await get_session_repository(session=session)

    return AuthService(
        user_repository=user_repository,
        profile_repository=profile_repository,
        session_repository=session_repository,
    )