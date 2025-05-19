from typing import Annotated, List

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api_v1.home.dependency import get_home_service
from api_v1.home.schema import HomeCreateRequest, GetHomeRequest, AddDeviceRequest
from api_v1.home.service import HomeService
from api_v1.session.dependency import get_session_service
from api_v1.session.schema import SessionCreate
from api_v1.session.service import SessionService

router = APIRouter(tags=["home"])
http_bearer = HTTPBearer()

@router.get("", dependencies=[Depends(http_bearer)], response_model=List[GetHomeRequest])
async def get_home_list(home_service: Annotated[HomeService, Depends(get_home_service)]):
    return await home_service.get_home_list()


@router.get("/{home_id}", dependencies=[Depends(http_bearer)], response_model=GetHomeRequest)
async def get_home_by_id(home_id: int, home_service: Annotated[HomeService, Depends(get_home_service)]):
    return await home_service.get_home_by_id(home_id=home_id)


@router.post("/accessible", dependencies=[Depends(http_bearer)])
async def get_home_list_by_user_id(
        session_service: Annotated[SessionService, Depends(get_session_service)],
        home_service: Annotated[HomeService, Depends(get_home_service)],
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    current_session = await session_service.get_session_by_access_token(credentials=credentials)
    user_id = SessionCreate(**current_session).user_id
    return await home_service.get_home_list_by_user_id(user_id=user_id)


@router.post("", dependencies=[Depends(http_bearer)])
async def create_home(
        created_home: HomeCreateRequest,
        home_service: Annotated[HomeService, Depends(get_home_service)]
):
    return await home_service.create_home(created_home=created_home)


@router.post("/device", dependencies=[Depends(http_bearer)])
async def add_device_in_home(
    home_service: Annotated[HomeService, Depends(get_home_service)],
    added_device: AddDeviceRequest
):

    return await home_service.add_device_in_home(added_device=added_device)