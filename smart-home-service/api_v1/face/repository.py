import base64
import io
from dataclasses import dataclass

import face_recognition
import numpy as np
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from PIL import Image
from starlette.concurrency import run_in_threadpool

from api_v1.face.model import Face
from api_v1.face.schema import FaceForm, GetFace


@dataclass
class FaceRepository:
    db_session: AsyncSession

    async def get_item_face_by_home_id(self, home_id: int) -> list[GetFace]:
        result = await self.db_session.execute(select(Face).where(Face.home_id == home_id))
        return result.scalars().all()

    async def create_face(self, face_request: FaceForm):
        try:
            img_bytes = base64.b64decode(face_request.file)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Невалидная Base64-строка изображения"
            )

        def compute_encodings(data: bytes):
            img = Image.open(io.BytesIO(data))
            arr = np.array(img)
            return face_recognition.face_encodings(arr)

        encodings = await run_in_threadpool(compute_encodings, img_bytes)
        if not encodings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Лицо не обнаружено на изображении"
            )

        embedding = encodings[0].tolist()
        face = Face(
            name=face_request.name,
            home_id=face_request.home_id,
            embedding=embedding
        )
        self.db_session.add(face)
        await self.db_session.commit()