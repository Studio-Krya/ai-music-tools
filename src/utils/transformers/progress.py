from transformers.generation.streamers import BaseStreamer
from typing import Awaitable, Callable, Any
from tqdm import tqdm
import threading
import asyncio

class BaseProgressStreamer(BaseStreamer):
    def __init__(self, total_steps: int, on_progress: Callable[[float, float, float], Awaitable[Any]]):
        # self.pbar = tqdm(total=total_steps + 1, desc="Test", unit="step")

        self.steps = 0
        self.total_steps = total_steps
        self.on_progress = on_progress
        

    def _progress_thread(self, on_progress: Callable[[float, float, float], Awaitable[Any]], progress: float, steps: int, total_steps: int):
        asyncio.run(on_progress(progress, steps, total_steps))

    def broadcast(self, progress: float, steps: int, total_steps: int):
        if self.on_progress is not None:
            threading.Thread(target=self._progress_thread, args=(self.on_progress, progress, steps, total_steps), daemon=True).start()
        

    def put(self, value):
        self.steps += 1
        self.broadcast(min(self.steps / self.total_steps * 100, 100), self.steps, self.total_steps)
        # self.pbar.update(1)

        # if self.on_progress is not None:
        #     progress = min(self.steps / self.total_steps * 100, 100)
        #     self.on_progress(progress, self.steps, self.total_steps)

    def end(self):
        self.broadcast(100, self.steps, self.total_steps)
        # self.pbar.close()

# class TqdmProgressStreamer(BaseStreamer):
#     def __init__(self, title: str, total_steps: int):
#         self.pbar = tqdm(total=total_steps + 1, desc=title, unit="step")

#     def put(self, value):
#         self.pbar.update(1)

#     def end(self):
#         self.pbar.close()

# class APIProgressStreamer(BaseStreamer):
#     def __init__(self, total_steps: int, on_progress: Callable[[float], None]):
#         self.steps = 0
#         self.total_steps = total_steps
#         self.on_progress = on_progress

#     def put(self, value):
#         self.steps += 1
#         progress = min(self.steps / self.total_steps * 100, 100)
#         self.on_progress(progress)

#     def end(self):
#         pass