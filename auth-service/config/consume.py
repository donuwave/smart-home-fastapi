import json
from api_v1.auth.dependency import get_auth_service
from api_v1.auth.schema import LoginRequest, RegistrationRequest, RefreshRequest, LogoutRequest
from api_v1.profile.dependency import get_profile_service
from api_v1.profile.schema import ProfileGetResponse
from api_v1.session.dependency import get_session_service
from api_v1.session.schema import SessionResponse
from config.database import db_helper
from config.settings import Settings
import aio_pika
from pydantic import EmailStr

settings = Settings()

async def callback_message(correlation_id: str, body: dict):
    connection = await aio_pika.connect_robust(settings.AMQP_URL)
    async with connection:
        channel = await connection.channel()

        message = aio_pika.Message(
            body=json.dumps(body).encode(),
            correlation_id=correlation_id,
        )
        await channel.default_exchange.publish(
            message=message,
            routing_key="callback_auth_queue"
        )

async def pick_service(key: str, body: dict | int | str | EmailStr) -> dict | int:
    service = key.split(".")[0]
    handler = key.split(".")[1]
    session = await db_helper.scoped_session_dependency()

    if service == "auth":
        auth_service = await get_auth_service(session=session)

        if handler == "login":
            login_result = await auth_service.login(login_request=LoginRequest(**body))
            return dict(login_result)

        if handler == "registration":
            registration_result = await auth_service.registration(register_request=RegistrationRequest(**body))
            return dict(registration_result)

        if handler == "refresh":
            refresh_result = await auth_service.refresh(refresh_request=RefreshRequest(**body))
            return dict(refresh_result)

        if handler == 'logout':
            logout_result = await auth_service.logout(logout_request=LogoutRequest(**body))
            return logout_result

    if service == "profile":
        profile_service = await get_profile_service(session=session)

        if handler == 'get_profile_by_id':
            profile = await profile_service.get_profile_by_id(profile_id=body)
            return ProfileGetResponse.model_validate(profile).model_dump()

    if service == "session":
        session_service = await get_session_service(session=session)

        if handler == "get_session":
            result = await session_service.get_session(session_id=body)
            return SessionResponse.model_validate(result).model_dump()

    return dict()


async def consume_message(message: aio_pika.IncomingMessage):
    async with message.process():
        raw_body = json.loads(message.body.decode())
        key = raw_body.get("key")
        body = raw_body.get("body")

        try:
            result = await pick_service(key=key, body=body)
            await callback_message(correlation_id=message.correlation_id, body=result)
        except Exception as e:
            print(e)
            error_response = {"status": "error", "message": str(e)}
            await callback_message(correlation_id=message.correlation_id, body=error_response)

async def make_broker_consumer():
    connection = await aio_pika.connect_robust(settings.AMQP_URL)
    chanel = await connection.channel()
    queue = await chanel.declare_queue("auth_queue", durable=True)
    await queue.consume(consume_message)