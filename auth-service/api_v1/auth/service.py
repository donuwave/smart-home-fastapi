from dataclasses import dataclass

from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.schema import RegistrationRequest, AuthResponse, LoginRequest
from api_v1.auth.utils import (
    hash_password,
    create_access_token,
    create_refresh_token,
    validate_password,
    decode_jwt,
    validate_token_type,
    REFRESH_TOKEN_TYPE,
    ACCESS_TOKEN_TYPE,
)
from api_v1.profile.repository import ProfileRepository
from api_v1.profile.schema import ProfileCreateRequest
from api_v1.session.repository import SessionRepository
from api_v1.session.schema import SessionCreate, SessionUpdate
from api_v1.user.repository import UserRepository
from api_v1.user.schema import UserCreate


@dataclass
class AuthService:
    db_session: AsyncSession
    user_repository: UserRepository
    profile_repository: ProfileRepository
    session_repository: SessionRepository

    async def login(self, login_request: LoginRequest) -> AuthResponse:
        user = await self.user_repository.get_user_by_email(email=login_request.email)

        authed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not user:
            raise authed_exc

        if not await validate_password(
            password_user=login_request.password, hashed_password=user.password
        ):
            raise authed_exc

        access_token = await create_access_token(user_id=user.id)
        refresh_token = await create_refresh_token(user_id=user.id)

        session_req = SessionCreate(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            device_id=login_request.device_id,
        )
        await self.session_repository.create_session(session=session_req)

        return AuthResponse(
            access_token=access_token, refresh_token=refresh_token, user_id=user.id
        )

    async def registration(self, register_request: RegistrationRequest) -> AuthResponse:
        existing_user = await self.user_repository.get_user_by_email(
            email=register_request.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь с текущим почтовым ящиком уже существует",
            )

        profile_request_data = ProfileCreateRequest(
            email=register_request.email, gender=None
        )
        profile_id = await self.profile_repository.create_profile(
            profile_create=profile_request_data
        )

        hashed_password = await hash_password(password_user=register_request.password)

        user_create_data = UserCreate(
            email=register_request.email,
            password=hashed_password,
            profile_id=profile_id,
        )
        user_id = await self.user_repository.create_user(user_create=user_create_data)

        access_token = await create_access_token(user_id=user_id)
        refresh_token = await create_refresh_token(user_id=user_id)

        session_req = SessionCreate(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            device_id=register_request.device_id,
        )
        await self.session_repository.create_session(session=session_req)

        return AuthResponse(
            access_token=access_token, refresh_token=refresh_token, user_id=user_id
        )

    async def refresh(self, credentials: HTTPAuthorizationCredentials) -> AuthResponse:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Токен отсутствует")

        refresh_token = credentials.credentials
        payload = await decode_jwt(token=refresh_token)
        await validate_token_type(token_type=REFRESH_TOKEN_TYPE, payload=payload)

        user_id = payload.get("user_id")
        user = self.user_repository.get_user_by_id(user_id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Токен не найден"
            )

        access_token = await create_access_token(user_id=user_id)

        current_session = await self.session_repository.get_session_by_refresh_token(
            refresh_token=refresh_token
        )

        session_req = SessionUpdate(
            session_id=current_session.id, access_token=access_token
        )
        await self.session_repository.update_session(session=session_req)

        return AuthResponse(
            access_token=access_token, refresh_token=refresh_token, user_id=user_id
        )

    async def logout(self, credentials: HTTPAuthorizationCredentials):
        if credentials is None:
            raise HTTPException(status_code=401, detail="Токен отсутствует")

        access_token = credentials.credentials
        payload = await decode_jwt(token=access_token)
        await validate_token_type(token_type=ACCESS_TOKEN_TYPE, payload=payload)

        session = await self.session_repository.get_session_by_access_token(
            access_token=access_token
        )

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Сессия не найдена"
            )

        await self.session_repository.delete_session(session=session)
