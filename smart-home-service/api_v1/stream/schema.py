from pydantic import BaseModel


class PushParams(BaseModel):
    token: str
    title: str
    body: str
    home_id: int