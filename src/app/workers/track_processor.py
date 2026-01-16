from typing import Any

from src.core.database import AsyncSession
from src.core.queue import Queue, QueueMessage

from src.providers.audiocraft.service import AudiocraftService
from src.providers.audiocraft.dtos import MusicGenParams
from src.app.tracks.service import TrackService

from src.utils.decorators import async_throttle
from src.app.tracks.jobs.service import TrackJobService
from src.app.tracks.jobs.dtos import TrackWorkerPayload
from src.utils.file import get_base_url

class TrackProcessor:
    __queue_name__ = "track_processor"
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.queue = Queue[TrackWorkerPayload](self.__queue_name__)
        self.track_service = TrackService(db)
        self.track_job_service = TrackJobService(db)

    @staticmethod
    def produce(payload: TrackWorkerPayload):
        queue = Queue[TrackWorkerPayload](TrackProcessor.__queue_name__)
        queue.put(payload)

    async def process(self, message: QueueMessage[TrackWorkerPayload]):
        data = message.data
        print(f"✓ Processing message: {data}")

        track = await self.track_service.get_by_id(data.track_id)

        if track is None:
            print(f"✓ Track not found: {data.track_id}")
            return

        @async_throttle(0.5)
        async def on_progress(progress: float, steps: int, total_steps: int):
            await self.track_job_service.update_job_progress(data.job_id, progress)

        params = MusicGenParams(
            prompt=track.prompt,
            duration=track.duration,
            model=track.model,
            on_progress=on_progress
        )   

        file_path = AudiocraftService().generate_music(params)
        job = await self.track_job_service.update_job_progress(data.job_id, 100)
        
        track.audio_url = job.artifact_url = get_base_url(file_path)

        await self.track_service.update(track)
        await self.track_job_service.update(job)

        print(f"✓ Generated: {track.audio_url}")
        self.queue.done(message.message_id)
        pass