from fastapi import APIRouter
from fastapi.params import Depends
from typing import Annotated

from fastapi.security import HTTPBearer

from api_v1.profile.dependency import get_profile_service
from api_v1.profile.service import ProfileService

router = APIRouter(tags=["profile"])
http_bearer = HTTPBearer()


@router.get("", dependencies=[Depends(http_bearer)])
async def get_profile(profile_id: int, profile_service: Annotated[ProfileService, Depends(get_profile_service)]):
    return await profile_service.get_profile_by_id(profile_id=profile_id)
