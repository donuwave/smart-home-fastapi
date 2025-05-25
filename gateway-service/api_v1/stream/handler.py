import httpx
from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBearer
from starlette.responses import StreamingResponse

from settings import app_settings

router = APIRouter(tags=["stream"])
http_bearer = HTTPBearer()

@router.get("/video_feed")
async def video_feed(
    device_id: int,
):
    async def proxy_iterator():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                    "GET",
                    f"{app_settings.SMART_HOME_SERVICE_URL}/api/v1/stream/video_feed",
                    params={"device_id": device_id }
            ) as upstream:
                if upstream.status_code != 200:
                    body = await upstream.aread()
                    raise HTTPException(
                        status_code=upstream.status_code,
                        detail=body.decode(errors="ignore")
                    )
                async for chunk in upstream.aiter_bytes():
                    yield chunk

    return StreamingResponse(
        proxy_iterator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )