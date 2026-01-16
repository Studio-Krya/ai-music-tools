from src.core.database import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional, List

from .jobs.model import TrackJob

class Track(BaseModel, table=True):
    __tablename__ = 'tracks'

    name: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=300)
    category: Optional[str] = Field(max_length=100)
    prompt: str = Field(max_length=300)
    model: Optional[str] = Field(max_length=100)
    provider: Optional[str] = Field(max_length=100)
    duration: int = Field(default=10)
    audio_url: Optional[str] = Field(max_length=300)
    jobs: List[TrackJob] = Relationship()