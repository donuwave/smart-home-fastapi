from typing import List, Optional

from pydantic import BaseModel


class HomeCreateRequest(BaseModel):
    name: str
    address: str
    owner_id: int

class GetHomeResponse(BaseModel):
    id: int
    name: str
    address: str
    owner_id: int
    invited_users_ids: Optional[List[int]]

    class Config:
        from_attributes = True