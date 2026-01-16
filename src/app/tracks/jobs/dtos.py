from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum
from typing import Optional
import uuid

class TrackJobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TrackJobDTO(BaseModel):
    id: uuid.UUID
    track_id: uuid.UUID
    status: TrackJobStatus
    progress: float
    artifact_url: Optional[str] = None

class CreateTrackJobDTO(BaseModel):
    track_id: uuid.UUID
    status: Optional[TrackJobStatus] = TrackJobStatus.PENDING
    progress: Optional[float] = 0.0
    artifact_url: Optional[str] = None

@dataclass
class TrackWorkerPayload:
    track_id: str
    job_id: str