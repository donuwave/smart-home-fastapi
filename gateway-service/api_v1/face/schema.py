from fastapi import UploadFile, File, Form
from pydantic import BaseModel


class FaceForm(BaseModel):
    name: str
    file: UploadFile
    home_id: int


async def face_form(
    name: str = Form(...),
    home_id: int = Form(...),
    file: UploadFile = File(...),
):
    return FaceForm(name=name, file=file, home_id=home_id)
