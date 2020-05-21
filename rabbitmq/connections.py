import aio_pika


async def connect(loop):
    conn = await aio_pika.connect_robust(
        "amqp://pmotos:pmotos@localhost/", loop=loop
    )

    return conn

