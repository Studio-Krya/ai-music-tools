from pydantic import BaseModel
from typing import Optional
from .jobs.dtos import TrackJobDTO
from typing import List

import uuid
from datetime import datetime

class CreateTrackDTO(BaseModel):
    name: str
    prompt: str
    description: Optional[str] = None
    category: Optional[str] = None
    model: Optional[str] = "facebook/musicgen-small"
    provider: Optional[str] = "audiocraft"
    duration: Optional[int] = 5

class TrackDTO(CreateTrackDTO):
    id: uuid.UUID
    audio_url: Optional[str] = None
    jobs: Optional[List[TrackJobDTO]] = []
    created_at: datetime
    updated_at: datetime
