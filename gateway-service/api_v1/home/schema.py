from typing import List

from pydantic import BaseModel


class HomeCreateRequest(BaseModel):
    name: str
    address: str
    owner_id: int
    invited_users_ids: List[int]