from typing import Annotated

from fastapi import APIRouter, Depends

from api_v1.user.dependency import get_user_service
from api_v1.user.schema import UserCreate
from api_v1.user.service import UserService

router = APIRouter()


@router.post("")
async def create_user(
    body: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(user_create=body)


@router.get("")
async def get_user_by_id(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_user_by_id(user_id=user_id)
