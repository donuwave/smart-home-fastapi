import json
from config.pick_service import pick_service
from config.settings import Settings
import aio_pika

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
            routing_key="callback_notification_queue"
        )


async def consume_message(message: aio_pika.IncomingMessage):
    async with message.process():
        raw_body = json.loads(message.body.decode())
        key = raw_body.get("key")
        body = raw_body.get("body")

        try:
            result = await pick_service(key=key, body=body)
            await callback_message(correlation_id=message.correlation_id, body=result)
        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            await callback_message(correlation_id=message.correlation_id, body=error_response)

async def make_broker_consumer():
    connection = await aio_pika.connect_robust(settings.AMQP_URL)
    chanel = await connection.channel()
    queue = await chanel.declare_queue("notification_queue", durable=True)
    await queue.consume(consume_message)