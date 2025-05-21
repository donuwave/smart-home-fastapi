from typing import Annotated

from fastapi import APIRouter, Depends

from api_v1.stream.dependency import get_stream_service
from api_v1.stream.service import StreamService

router = APIRouter(tags=["stream"])

@router.get("/video_feed")
async def video_feed(stream_service: Annotated[StreamService, Depends(get_stream_service)], home_id: int, device_id: int):
    return await stream_service.video_feed(home_id=home_id, device_id=device_id)
