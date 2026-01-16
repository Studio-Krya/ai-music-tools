from fastapi import Depends
from typing import List, Any
from sqlmodel import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from src.core.database import async_get_db, AsyncSession
from src.core.repository import BaseRepository

from .model import Track
from .jobs.service import TrackJobService
# from .jobs.dtos import GenerateAudioTrackJobDTO

class TrackService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.job_service = TrackJobService(db)
        self.repository = BaseRepository[Track](Track, db, [selectinload(Track.jobs)])

    async def get_all(self) -> List[Track]:
        return await self.repository.get_all(sort_by="created_at", sort_order="desc")

    async def get_by_id(self, id: str) -> Track:
        return await self.repository.get_by_id(id)

    async def create(self, track: Any) -> Track:
        track = Track(
            name=track.name, 
            description=track.description, 
            prompt=track.prompt,
            category=track.category, 
            duration=track.duration,
            model=track.model,
            provider=track.provider,
            audio_url=None,
        )

        track = await self.repository.create(track)

        await self.job_service.generate_audio(track)

        return await self.get_by_id(track.id)

    async def update(self, track: Track) -> Track:
        track.updated_at = datetime.now()
        return await self.repository.update(track)


def get_track_service(db: AsyncSession = Depends(async_get_db)) -> TrackService:
    return TrackService(db)