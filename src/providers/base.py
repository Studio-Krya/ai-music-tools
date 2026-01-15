"""Base provider utilities."""
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def get_default_output(provider_name: str, file_name: str = "output") -> Path:
    """Get default output path for a provider."""
    # Use storage/output relative to project root
    output_dir = Path(__file__).parent.parent.parent / "storage" / provider_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / file_name


def run_command(
    command: List[str],
    raw_cli: bool = False,
    additional_args: Optional[List[str]] = None,
) -> int:
    """Run a command with optional additional arguments."""
    if additional_args:
        command.extend(additional_args)
    
    if raw_cli:
        # Skip normalization, just pass through
        pass
    
    try:
        # SHould suppress output
        result = subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode
    except Exception as e:
        print(f"Error running command: {e}", file=sys.stderr)
        return 1
