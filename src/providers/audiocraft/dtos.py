"""Data models for Audiocraft provider."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class MusicGenParams:
    """Parameters for MusicGen generation."""
    prompt: str
    output: Optional[Path] = None
    model: str = "facebook/musicgen-small"
    duration: int = 10
    temperature: float = 1.0


@dataclass
class AudioGenParams:
    """Parameters for AudioGen generation."""
    prompt: str
    output: Optional[Path] = None
    model: str = "facebook/audiogen-medium"
    duration: int = 10
