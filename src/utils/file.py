"""Base provider utilities."""
from pathlib import Path
from typing import Optional
import uuid


def get_folder_output(provider_name: str, file_name: Optional[str] = None) -> str:
    output_dir = Path(__file__).parent.parent.parent / "storage" / provider_name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_filename = file_name if file_name else f"{uuid.uuid4()}.wav"
    return str(output_dir / output_filename)

def get_base_url(file_path: str) -> str:
    base_dir = str(Path(__file__).parent.parent.parent)
    return file_path.replace(base_dir, "")
