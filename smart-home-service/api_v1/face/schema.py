from pydantic import BaseModel


class FaceForm(BaseModel):
    name: str
    file: bytes
    home_id: int


class GetFace(BaseModel):
    home_id: int
    name: str
    embedding: list[float]