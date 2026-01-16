from pydantic import BaseModel
from typing import Optional
from .jobs.dtos import TrackJobDTO
from typing import List

import uuid

class CreateTrackDTO(BaseModel):
    name: str
    prompt: str
    description: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[int] = 5

class TrackDTO(BaseModel):
    id: uuid.UUID
    name: str
    prompt: str
    description: Optional[str] = None
    category: Optional[str] = None
    duration: int
    audio_url: Optional[str] = None
    jobs: Optional[List[TrackJobDTO]] = []
