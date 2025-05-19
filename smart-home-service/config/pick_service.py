from api_v1.device.dependency import get_device_service
from api_v1.device.schema import GetDeviceResponse, CreateDeviceRequest
from api_v1.home.dependency import get_home_service
from api_v1.home.schema import HomeCreateRequest, GetHomeResponse, AddDeviceRequest
from config.database import db_helper
from pydantic import EmailStr

async def pick_service(key: str, body: dict | int | str | EmailStr) -> list | dict[str, dict]:
    service = key.split(".")[0]
    handler = key.split(".")[1]
    session = await db_helper.scoped_session_dependency()

    if service == "home":
        home_service = await get_home_service(session=session)

        if handler == 'get_home_list':
            home_list = await home_service.get_home_list()
            return [
                GetHomeResponse.model_validate(home_item).model_dump()
                for home_item in home_list
            ]

        if handler == 'get_home_by_id':
            home = await home_service.get_home_by_id(home_id=body)
            return GetHomeResponse.model_validate(home).model_dump()

        if handler == 'get_home_list_by_user_id':
            home_list = await home_service.get_home_list_by_user_id(user_id=body)
            return [
                GetHomeResponse.model_validate(home_item).model_dump()
                for home_item in home_list
            ]

        if handler == "create_home":
            return await home_service.create_home(created_home=HomeCreateRequest(**body))


        if handler == 'add_device_in_home':
            return await home_service.add_device_in_home(added_device=AddDeviceRequest(**body))

    if service == "device":
        device_service = await get_device_service(session=session)

        if handler == 'get_list_device_in_home':
            device_list = await device_service.get_list_device_in_home(home_id=body)
            return [
                GetDeviceResponse.model_validate(device_item).model_dump()
                for device_item in device_list
            ]

        if handler == 'get_item_device_in_home':
            device_item = await device_service.get_item_device_in_home(device_id=body)
            return GetDeviceResponse.model_validate(device_item).model_dump()

        if handler == 'create_device':
            await device_service.create_device(created_device=CreateDeviceRequest(**body))


    return dict()
