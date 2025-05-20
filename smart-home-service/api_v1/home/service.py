from dataclasses import dataclass

from api_v1.home.repository import HomeRepository
from api_v1.home.schema import HomeCreateRequest, GetHomeResponse, AddDeviceRequest


@dataclass
class HomeService:
    home_repository: HomeRepository

    async def get_home_list(self) -> list[GetHomeResponse]:
        return await self.home_repository.get_home_list()


    async def get_home_by_id(self, home_id: int):
        return await self.home_repository.get_home_by_id(home_id=home_id)


    async def get_home_list_by_user_id(self, user_id: int) -> list[GetHomeResponse]:
        return await self.home_repository.get_home_list_by_user_id(user_id=user_id)


    async def create_home(self, created_home: HomeCreateRequest):
        return await self.home_repository.create_home(created_home=created_home)
