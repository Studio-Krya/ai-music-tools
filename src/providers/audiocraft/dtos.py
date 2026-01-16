from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Optional
from typing import Callable

from src.app.tracks.dtos import TrackDTO

@dataclass
class MusicGenParams:
    """Parameters for MusicGen generation."""
    prompt: str
    duration: int = 5
    model: str = "facebook/musicgen-small"
    temperature: float = 1.0
    on_progress: Optional[Callable[[float, float, float], Awaitable[Any]]] = None
    
@dataclass
class AudioGenParams:
    """Parameters for AudioGen generation."""
    prompt: str
    output: Optional[Path] = None
    model: str = "facebook/audiogen-medium"
    duration: int = 10
