import json
import uuid

import aio_pika

from settings import app_settings

async def connection_broker(queue_name: str, queue_name_callback: str, body: dict):
    connection = await aio_pika.connect_robust(app_settings.AMQP_URL)

    try:
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(queue_name, durable=True)

            callback_queue = await channel.declare_queue(queue_name_callback, exclusive=True)
            correlation_id = str(uuid.uuid4())

            message = aio_pika.Message(
                body=json.dumps(body).encode(),
                correlation_id=correlation_id,
                reply_to=callback_queue.name
            )
            await channel.default_exchange.publish(
                message=message,
                routing_key=queue_name
            )

            async with callback_queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        if message.correlation_id == correlation_id:
                            result = json.loads(message.body.decode())
                            return result
    except Exception as e:
        return e