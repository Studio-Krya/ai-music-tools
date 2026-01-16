# worker.py
import asyncio
from typing import Any, Callable
from src.core.database import AsyncSession

from .track_processor import TrackProcessor
import threading
POLL = 1

QUEUES = [
    TrackProcessor,
]

def run_in_bg(process: Callable[[Any], Any], message: Any):
    print(f"✓ Running in background: {message}")
    asyncio.run(process(message))

    
async def listen(db: AsyncSession, stop: asyncio.Event):
    workers = [queue(db) for queue in QUEUES]

    for worker in workers:
        print(f"✓ Listening to queue: {worker.__queue_name__}")

    while not stop.is_set():
        for worker in workers:
            message = worker.queue.pop()
            if message is not None:
                threading.Thread(target=run_in_bg, args=(worker.process, message), daemon=True).start()

                # asyncio.create_task(run_in_bg(worker.process, message))
                # await asyncio.sleep(15)
                # asyncio.create_task(worker.process(message))

        await asyncio.sleep(POLL)
