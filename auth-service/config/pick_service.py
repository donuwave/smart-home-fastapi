from api_v1.auth.dependency import get_auth_service
from api_v1.auth.schema import LoginRequest, RegistrationRequest, RefreshRequest, LogoutRequest
from api_v1.profile.dependency import get_profile_service
from api_v1.profile.schema import ProfileGetResponse
from api_v1.session.dependency import get_session_service
from api_v1.session.schema import SessionResponse, SessionUpdateFCMTokenParams, SessionByAccessToken, \
    SessionUpdateHomeIdParams
from config.database import db_helper
from pydantic import EmailStr

async def pick_service(key: str, body: dict | int | str | EmailStr) -> list | dict[str, dict]:
    service = key.split(".")[0]
    handler = key.split(".")[1]
    session = await db_helper.scoped_session_dependency()

    if service == "auth":
        auth_service = await get_auth_service(session=session)

        if handler == "login":
            login_result = await auth_service.login(login_request=LoginRequest(**body))
            return dict(login_result)

        if handler == "registration":
            registration_result = await auth_service.registration(register_request=RegistrationRequest(**body))
            return dict(registration_result)

        if handler == "refresh":
            refresh_result = await auth_service.refresh(refresh_request=RefreshRequest(**body))
            return dict(refresh_result)

        if handler == 'logout':
            logout_result = await auth_service.logout(logout_request=LogoutRequest(**body))
            return logout_result

    if service == "profile":
        profile_service = await get_profile_service(session=session)

        if handler == 'get_profile_by_id':
            profile = await profile_service.get_profile_by_id(profile_id=body)
            return ProfileGetResponse.model_validate(profile).model_dump()

    if service == "session":
        session_service = await get_session_service(session=session)

        if handler == "get_session":
            result = await session_service.get_session(session_id=body)
            return SessionResponse.model_validate(result).model_dump()

        if handler == "get_list_session":
            result = await session_service.get_list_session(access_token=body)

            return [
                SessionResponse.model_validate(session).model_dump()
                for session in result
            ]

        if handler == "get_list_session_by_home_id":
            result = await session_service.get_list_session_by_home_id(home_id=body)

            return [
                SessionResponse.model_validate(session).model_dump()
                for session in result
            ]


        if handler == 'get_session_by_access_token':
            result = await session_service.get_session_by_access_token(access_token=body)
            return SessionByAccessToken.model_validate(result).model_dump()

        if handler == "patch_session_home_id":
            await session_service.patch_session_home_id(session_params=SessionUpdateHomeIdParams(**body))

        if handler == "patch_session_fcm_token":
            await session_service.patch_session_fcm_token(session_params=SessionUpdateFCMTokenParams(**body))

    return dict()
