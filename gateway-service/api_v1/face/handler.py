from typing import Annotated

from fastapi import APIRouter, Depends

from api_v1.face.dependency import get_face_service
from api_v1.face.schema import face_form
from api_v1.face.service import FaceService

router = APIRouter(tags=["face"])


@router.post("")
async def create_face(
    face_service: Annotated[FaceService, Depends(get_face_service)],
    data=Depends(face_form),
):
    return await face_service.create_face(face_request=data)

