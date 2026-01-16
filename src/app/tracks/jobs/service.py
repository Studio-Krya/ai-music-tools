from functools import wraps
from fastapi import Depends
from typing import List

from src.core.database import async_get_db, AsyncSession
from src.core.repository import BaseRepository
from src.app.tracks.dtos import TrackDTO

from .model import TrackJob, TrackJobStatus
from .dtos import CreateTrackJobDTO

from src.app.tracks.jobs.dtos import TrackWorkerPayload

class TrackJobService:

    def __init__(self, db: AsyncSession):
        self.repository = BaseRepository[TrackJob](TrackJob, db)
        self.db = db

    async def get_all(self) -> List[TrackJob]:
        return await self.repository.get_all()

    async def get_by_id(self, id: str) -> TrackJob:
        return await self.repository.get_by_id(id)

    async def create(self, job: CreateTrackJobDTO) -> TrackJob:
        job = TrackJob(
            track_id=job.track_id,
            status=job.status,
            progress=job.progress,
            artifact_url=job.artifact_url
        )

        return await self.repository.create(job)
    
    async def update(self, job: TrackJob) -> TrackJob:
        return await self.repository.update(job)
    
    async def update_job_progress(self, jobId: str, progress: float):
        print(f"Updating job progress: {jobId} | {progress}")

        job = await self.repository.get_one_by_id(jobId)
        print(f"Job: {job}")
        job
        job.progress = progress

        if progress == 100:
            job.status = TrackJobStatus.COMPLETED
        elif progress > 0:
            job.status = TrackJobStatus.PROCESSING
        else:
            job.status = TrackJobStatus.PENDING

        return await self.repository.update(job)

    async def generate_audio(self, track: TrackDTO) -> TrackJob:
        job = CreateTrackJobDTO(
            track_id=track.id,
            status=TrackJobStatus.PENDING,
            progress=0.0,
            artifact_url=None
        )

        job = await self.create(job)
        
        from src.app.workers.track_processor import TrackProcessor
        TrackProcessor.produce(TrackWorkerPayload(track_id=str(track.id), job_id=str(job.id)))
      


def get_track_job_service(db: AsyncSession = Depends(async_get_db)) -> TrackJobService:
    return TrackJobService(db)
