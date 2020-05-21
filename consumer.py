import asyncio
import sys

import argparse

from rabbitmq import queues


__AVAILABLE_WORKERS__ = {
    'tokens': queues.Tokens,
     'images': queues.Images
}

parser = argparse.ArgumentParser()
parser.add_argument(
    'worker',
    type=str,
)
args= parser.parse_args()


def get_worker(worker_name):
    worker = __AVAILABLE_WORKERS__.get(worker_name)
    if worker is None:
        print(f'Error: worker {worker_name} doesnt exists!')
        print('Available workers:')

        for key in __AVAILABLE_WORKERS__.keys():
            print(f'\t{key}')

        sys.exit(2)

    consumer = worker(loop)

    return consumer


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    worker = get_worker(args.worker)
    connection = loop.run_until_complete(worker.consume())

    print(f'worker: {args.worker} is running...')

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
