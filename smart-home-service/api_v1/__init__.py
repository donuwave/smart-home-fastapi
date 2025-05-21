from fastapi import APIRouter

from .stream import stream_router

router = APIRouter()
router.include_router(stream_router, prefix="/stream", tags=["stream"])