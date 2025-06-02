from pydantic import BaseModel


class PushParams(BaseModel):
    token: str
    home_id: int
    title: str
    body: str