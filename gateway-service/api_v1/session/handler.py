from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api_v1.session.dependency import get_session_service
from api_v1.session.service import SessionService

router = APIRouter(tags=["session"])
http_bearer = HTTPBearer()


@router.get("/session_id", dependencies=[Depends(http_bearer)])
async def get_session(
    session_id: int,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    return await session_service.get_session(session_id=session_id)

@router.get("", dependencies=[Depends(http_bearer)])
async def get_list_session(
        session_service: Annotated[SessionService, Depends(get_session_service)],
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await session_service.get_list_session(credentials=credentials)

@router.patch("", dependencies=[Depends(http_bearer)])
async def patch_session_fcm_token(
        session_service: Annotated[SessionService, Depends(get_session_service)],
        fcm_token: str,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await session_service.patch_session_fcm_token(credentials=credentials, fcm_token=fcm_token)