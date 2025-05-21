from api_v1.face.service import FaceService


async def get_face_service() -> FaceService:
    return FaceService()