from dataclasses import dataclass

from api_v1.session.repository import SessionRepository
from api_v1.session.schema import SessionResponse, SessionUpdateFCMTokenParams, SessionByAccessToken


@dataclass
class SessionService:
    session_repository: SessionRepository

    async def get_session(self, session_id: int) -> SessionResponse:
        return await self.session_repository.get_session_by_id(session_id=session_id)

    async def get_list_session(self, access_token: str) -> list[SessionResponse]:
        session = await self.session_repository.get_session_by_access_token(access_token=access_token)
        result = await self.session_repository.get_list_session_by_user_id(user_id=session.user_id)
        return result

    async def get_session_by_access_token(self, access_token: str) -> SessionByAccessToken:
        return await self.session_repository.get_session_by_access_token(access_token=access_token)

    async def patch_session_fcm_token(self, session_params: SessionUpdateFCMTokenParams):
        await self.session_repository.update_fcm_token_by_access_token(session_params)