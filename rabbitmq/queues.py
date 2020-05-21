import asyncio
import time
import json
import base64
from binascii import Error as PadddingError

import aio_pika
from rabbitmq.connections import connect
from rabbitmq.mail import Email


class BaseQueue():
    key = 'pamotos_token'

    def __init__(self, exchange_name, queue_name, loop):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.loop = loop

    async def _conn(self):
        conn = await connect(self.loop)
        return conn

    async def _channel(self, conn):
        chan = await conn.channel()
        return chan

    async def _exch(self, chan):
        _exch = await chan.declare_exchange(
            self.exchange_name, auto_delete=False
        )
        return _exch

    async def queue(self, chan):
        exch = await self._exch(chan)
        await exch.bind(self.exchange_name, self.key)
        _queue = await chan.declare_queue(
            self.queue_name, auto_delete=False
        )
        await _queue.bind(
            self.exchange_name, self.key
        )
        return _queue

    async def publish(self, msg):
        conn = await self._conn()
        chan = await self._channel(conn)
        exch = await self._exch(chan)

        return await exch.publish(
            aio_pika.Message(
                body=msg
            ),
            routing_key=self.key
        )

    async def consume(self):
        conn = await self._conn()
        chan = await self._channel(conn)
        _queue = await self.queue(chan)

        await _queue.consume(self.callback)

        return conn


class Tokens(BaseQueue):
    def __init__(self, loop):
        self.mail = Email()
        super().__init__('token_exch', 'tokens', loop)

    async def callback(self, message):
        print(f'[*] consuming {self.queue_name} queue...')
        json_msg = json.loads(message.body)
        print(f"Sending email to {json_msg['to']}")


        body = {
            'token': json_msg['token'],
            'expire_date': json_msg['expire_date']
        }

        self.mail.sendemail(
            json_msg['to'],
            json_msg['subject'],
            body,
        )
        await message.ack()


class Images(BaseQueue):
    def __init__(self, loop):
        self.mail = Email()
        super().__init__('images_exch', 'images', loop)

    async def callback(self, message):
        json_msg = json.loads(message.body)

        print(f'[*] consuming {self.queue_name} queue...')
        print(f"uploading img {json_msg['path']}")

        try:
            image_bytes = base64.b64decode(json_msg['image'].encode('utf-8'))
        except PadddingError:
            await message.ack()
            path = json_msg['path']
            print(f'[ERROR] Encoding error to file : {path}.')
        else:
            with open(json_msg['path'], 'wb') as _file:
                _file.write(image_bytes)

            await message.ack()

