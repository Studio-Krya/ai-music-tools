from fastapi.routing import APIRouter
from typing import List, Any, Optional
from fastapi import Depends
import uuid

from .model import Track

from .dtos import CreateTrackDTO, TrackDTO
from .service import TrackService, get_track_service
from .jobs.dtos import TrackJobDTO
from .jobs.routes import router as jobs_router

router = APIRouter(tags=["tracks"], prefix="/tracks")
router.include_router(jobs_router)

@router.get("", response_model=List[TrackDTO], status_code=200)
async def get_tracks(
    trackService: TrackService = Depends(get_track_service)
):
    tracks = await trackService.get_all()

    return [
        _track_to_dto(track) for track in tracks
    ]

@router.get("/{id}", response_model=Optional[TrackDTO], status_code=200)
async def get_track(
    id: uuid.UUID,
    trackService: TrackService = Depends(get_track_service)
):
    track = await trackService.get_by_id(id)
    return _track_to_dto(track)

@router.post("", response_model=TrackDTO, status_code=201)
async def create_track(
    track: CreateTrackDTO,
    trackService: TrackService = Depends(get_track_service)
):
    newTrack = await trackService.create(track)
    return _track_to_dto(newTrack)

def _track_to_dto(track: Track) -> TrackDTO:
    if(track is None):
        return None
    
    return TrackDTO(
        **track.model_dump(),
        jobs=[
            TrackJobDTO(
                **job.model_dump()
            ) for job in track.jobs
        ]
    )