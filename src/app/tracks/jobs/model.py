from src.core.database import BaseModel
from sqlmodel import Field
from typing import Optional
from enum import Enum
import uuid

class TrackJobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TrackJob(BaseModel, table=True):
    __tablename__ = 'track_jobs'
    
    track_id: uuid.UUID = Field(foreign_key='tracks.id')
    status: TrackJobStatus = Field(default=TrackJobStatus.PENDING, nullable=False)
    progress: float = Field(default=0)
    artifact_url: Optional[str] = Field(max_length=300) 