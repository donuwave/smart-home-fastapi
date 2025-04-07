import json
from typing import  Dict, Any
from api_v1.auth.dependency import get_auth_service
from api_v1.auth.schema import LoginRequest, RegistrationRequest
from config.database import db_helper
from config.settings import Settings
from pydantic import BaseModel
import aio_pika

settings = Settings()

class AuthEvent(BaseModel):
    key: str
    body: Dict[str, Any]


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

async def pick_service(key: str, body: dict):
    service = key.split(".")[0]
    handler = key.split(".")[1]
    session = await db_helper.scoped_session_dependency()
    print(key)

    if service == "auth":
        auth_service = await get_auth_service(session=session)

        if handler == "login":
            return await auth_service.login(login_request=LoginRequest(**body))

        if handler == "registration":
            return await auth_service.registration(register_request=RegistrationRequest(**body))


async def consume_message(message: aio_pika.IncomingMessage):
    async with message.process():
        raw_body = json.loads(message.body.decode())
        key = raw_body.get("key")
        body = raw_body.get("body")

        try:
            result = await pick_service(key=key, body=body)
            await callback_message(correlation_id=message.correlation_id, body=dict(result))
        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            await callback_message(correlation_id=message.correlation_id, body=error_response)

async def make_broker_consumer():
    connection = await aio_pika.connect_robust(settings.AMQP_URL)
    chanel = await connection.channel()
    queue = await chanel.declare_queue("auth_queue", durable=True)
    await queue.consume(consume_message)