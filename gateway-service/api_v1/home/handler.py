from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api_v1.home.dependency import get_home_service
from api_v1.home.schema import HomeCreateRequest
from api_v1.home.service import HomeService
from api_v1.session.dependency import get_session_service
from api_v1.session.service import SessionService

router = APIRouter(tags=["home"])
http_bearer = HTTPBearer()

@router.get("")
async def get_home_list(home_service: Annotated[HomeService, Depends(get_home_service)]):
    return await home_service.get_home_list()

@router.get("/{home_id}")
async def get_home_by_id(home_id: int, home_service: Annotated[HomeService, Depends(get_home_service)]):
    return home_service.get_home_by_id(home_id=home_id)

@router.post("/accessible", dependencies=[Depends(http_bearer)])
async def get_home_list_by_user_id(
        session_service: Annotated[SessionService, Depends(get_session_service)],
        home_service: Annotated[HomeService, Depends(get_home_service)],
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    current_session = await session_service.get_session_by_access_token(credentials=credentials)
    return await home_service.get_home_list_by_user_id(user_id=current_session)

@router.post("")
async def create_home(
        created_home: HomeCreateRequest,
        home_service: Annotated[HomeService, Depends(get_home_service)],
):
    pass