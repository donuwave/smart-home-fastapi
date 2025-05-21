from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.face.repository import FaceRepository
from api_v1.face.service import FaceService


async def get_face_repository(session: AsyncSession) -> FaceRepository:
    return FaceRepository(db_session=session)


async def get_face_service(session: AsyncSession) -> FaceService:
    face_repository: FaceRepository = await get_face_repository(session=session)
    return FaceService(face_repository=face_repository)