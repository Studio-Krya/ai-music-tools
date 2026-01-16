from fastapi.routing import APIRouter
from typing import List, Any
from fastapi import Depends
from .dtos import TrackJobDTO
from .service import TrackJobService, get_track_job_service
from .model import TrackJob

router = APIRouter(tags=["jobs"], prefix="/jobs")

@router.get("", response_model=List[TrackJobDTO])
async def get_jobs(jobService: TrackJobService = Depends(get_track_job_service)):
    jobs = await jobService.get_all()
    return [TrackJobDTO(**job.model_dump()) for job in jobs]

@router.get("/{id}", response_model=TrackJobDTO)
async def get_job(id: str, jobService: TrackJobService = Depends(get_track_job_service)):
    job = await jobService.get_by_id(id)
    return _job_to_dto(job)

def _job_to_dto(job: TrackJob) -> TrackJobDTO:
    if job is None:
        return {}
    
    return TrackJobDTO(
        **job.model_dump()
    )