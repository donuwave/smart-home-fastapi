from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.service import AuthService
from api_v1.profile.dependency import get_profile_repository
from api_v1.profile.repository import ProfileRepository
from api_v1.session.dependency import get_session_repository
from api_v1.session.repository import SessionRepository
from api_v1.user.dependency import get_user_repository
from api_v1.user.repository import UserRepository
from config.database import db_helper


async def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    profile_repository: Annotated[ProfileRepository, Depends(get_profile_repository)],
    session_repository: Annotated[SessionRepository, Depends(get_session_repository)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> AuthService:
    return AuthService(
        db_session=session,
        user_repository=user_repository,
        profile_repository=profile_repository,
        session_repository=session_repository,
    )
