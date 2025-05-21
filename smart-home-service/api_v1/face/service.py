from dataclasses import dataclass

from api_v1.face.repository import FaceRepository
from api_v1.face.schema import FaceForm


@dataclass
class FaceService:
    face_repository: FaceRepository

    async def create_face(self, face_request: FaceForm):
        return await self.face_repository.create_face(face_request=face_request)