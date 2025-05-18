from api_v1.home.dependency import get_home_service
from api_v1.home.schema import HomeCreateRequest, GetHomeResponse
from config.database import db_helper
from pydantic import EmailStr

async def pick_service(key: str, body: dict | int | str | EmailStr) -> list | dict[str, dict]:
    service = key.split(".")[0]
    handler = key.split(".")[1]
    session = await db_helper.scoped_session_dependency()

    if service == "home":
        session_service = await get_home_service(session=session)

        if handler == 'get_home_list':
            home_list = await session_service.get_home_list()
            return [
                GetHomeResponse.model_validate(home_item).model_dump()
                for home_item in home_list
            ]

        if handler == 'get_home_by_id':
            home = await session_service.get_home_by_id(home_id=body)
            return GetHomeResponse.model_validate(home).model_dump()

        if handler == 'get_home_list_by_user_id':
            home_list = await session_service.get_home_list_by_user_id(user_id=body)
            return [
                GetHomeResponse.model_validate(home_item).model_dump()
                for home_item in home_list
            ]

        if handler == "create_home":
            return await session_service.create_home(created_home=HomeCreateRequest(**body))

    return dict()
