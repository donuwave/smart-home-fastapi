from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api_v1.session.dependency import get_session_service
from api_v1.session.service import SessionService

router = APIRouter(tags=["session"])
http_bearer = HTTPBearer()


@router.get("", dependencies=[Depends(http_bearer)])
async def get_session(
    session_id: int,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    return await session_service.get_session(session_id=session_id)
