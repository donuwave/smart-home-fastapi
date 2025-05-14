from dataclasses import dataclass

from api_v1.session.repository import SessionRepository
from api_v1.session.schema import SessionResponse


@dataclass
class SessionService:
    session_repository: SessionRepository

    async def get_session(self, session_id: int) -> SessionResponse:
        return await self.session_repository.get_session_by_id(session_id=session_id)

    async def get_list_session(self, access_token: str) -> list[SessionResponse]:
        session = await self.session_repository.get_session_by_access_token(access_token=access_token)

        result = await self.session_repository.get_list_session_by_user_id(user_id=session.user_id)
        return result