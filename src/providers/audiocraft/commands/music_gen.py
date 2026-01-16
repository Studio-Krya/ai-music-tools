from typing import Optional
from pathlib import Path
import click
import sys

from ..commands import audiocraft_group
from ..dtos import MusicGenParams
from ..service import AudiocraftService

@audiocraft_group.command()
@click.argument("prompt", required=True)
@click.option("--model", "-m", default="facebook/musicgen-small", help="Model name")
@click.option("--duration", "-d", type=int, default=5, help="Duration in seconds")
def musicgen(
    prompt: str,
    model: str,
    duration: int,
):
    async def on_progress(progress: float, steps: int, total_steps: int):
        print(f"Progress: {progress}%")

    try:
        params = MusicGenParams(
            prompt=prompt,
            model=model,
            duration=duration,
            on_progress=on_progress,
        )
        
        output_path = AudiocraftService().generate_music(params)
        
        click.echo(f"✓ Generated: {output_path}")
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating music: {e}", err=True)
        sys.exit(1)