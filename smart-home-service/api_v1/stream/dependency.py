from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.device.dependency import get_device_repository
from api_v1.device.repository import DeviceRepository
from api_v1.face.dependency import get_face_repository
from api_v1.face.repository import FaceRepository
from api_v1.stream.service import StreamService
from config.database import db_helper


async def get_stream_service(session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)]) -> StreamService:
    device_repository: DeviceRepository = await get_device_repository(session=session)
    face_repository: FaceRepository = await get_face_repository(session=session)

    return StreamService(device_repository=device_repository, face_repository=face_repository)