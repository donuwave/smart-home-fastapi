from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from typing import Annotated, List

from api_v1.device.dependency import get_device_service
from api_v1.device.schema import GetDeviceResponse, CreateDeviceRequest
from api_v1.device.service import DeviceService

router = APIRouter(tags=["device"])
http_bearer = HTTPBearer()


@router.get("", dependencies=[Depends(http_bearer)] ,response_model=List[GetDeviceResponse])
async def get_list_device_in_home(
    device_service: Annotated[DeviceService, Depends(get_device_service)],
    home_id: int
):
    return await device_service.get_list_device_in_home(home_id=home_id)


@router.get("/{device_id}", dependencies=[Depends(http_bearer)], response_model=GetDeviceResponse)
async def get_item_device_in_home(
    device_service: Annotated[DeviceService, Depends(get_device_service)],
    device_id: int
):
    return await device_service.get_item_device_in_home(device_id=device_id)


@router.post("", dependencies=[Depends(http_bearer)])
async def create_device(
    device_service: Annotated[DeviceService, Depends(get_device_service)],
    created_device: CreateDeviceRequest
):
    return await device_service.create_device(created_device=created_device)