from pydantic import BaseModel


class GetDeviceResponse(BaseModel):
    id: int
    home_id: int
    device_type: str
    name: str
    model: str
    full_address: str

    class Config:
        from_attributes = True

class CreateDeviceRequest(BaseModel):
    home_id: int
    device_type: str
    name: str
    model: str
    full_address: str
