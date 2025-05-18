from api_v1.home.dependency import get_home_service
from config.database import db_helper
from pydantic import EmailStr

async def pick_service(key: str, body: dict | int | str | EmailStr) -> list | dict[str, dict]:
    service = key.split(".")[0]
    handler = key.split(".")[1]
    session = await db_helper.scoped_session_dependency()

    if service == "home":
        session_service = await get_home_service(session=session)

        if handler == 'get_home_list':
            return await session_service.get_home_list()

        if handler == 'get_home_by_id':
            return await session_service.get_home_by_id(home_id=body)

        if handler == 'get_home_list_by_user_id':
            return await session_service.get_home_list_by_user_id(user_id=body)

    return dict()
