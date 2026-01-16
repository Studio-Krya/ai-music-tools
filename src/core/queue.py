from dataclasses import asdict
import litequeue
import json
from typing import Any, Generic, TypeVar
from types import SimpleNamespace

from datetime import datetime

T = TypeVar('T')


class QueueMessage(litequeue.Message, Generic[T]):
    data: T

DB_QUEUE_PATH = "queue.db"

class Queue(Generic[T]):
    def __init__(self, name: str):
        self._queue = litequeue.LiteQueue(DB_QUEUE_PATH, queue_name=name)

    def put(self, data: T):
        json_data = json.dumps(asdict(data))
        self._queue.put(json_data)

    def pop(self) -> QueueMessage[T]:
        message = self._queue.pop()
        
        if message is None:
            return None

        return self._map_message(message)

    def peek(self) -> QueueMessage[T]:
        message = self._queue.peek()

        if message is None:
            return None

        return self._map_message(message)

    def done(self, message_id: str):
        self._queue.done(message_id)

    def _map_message(self, message: litequeue.Message) -> QueueMessage[T]:
        data = json.loads(message.data, object_hook=lambda d: SimpleNamespace(**d))
        return QueueMessage[T](**{**asdict(message), "data": data})
