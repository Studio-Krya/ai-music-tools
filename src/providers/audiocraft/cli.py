"""CLI definitions for Audiocraft provider."""
import click
import sys
from pathlib import Path
from typing import Optional

from src.providers.audiocraft.dtos import AudioGenParams, MusicGenParams
from src.providers.audiocraft.service import AudiocraftService


@click.group(invoke_without_command=True)
@click.option("--output", type=click.Path(), help="Output file path")
@click.pass_context
def audiocraft_group(ctx: click.Context, output: Optional[str]):
    if ctx.invoked_subcommand is None:
        click.echo("Audiocraft requires a subcommand. Use 'musicgen' or 'audiogen'")
        sys.exit(1)
    else:
        ctx.ensure_object(dict)
        ctx.obj["output"] = output


@audiocraft_group.command()
@click.argument("prompt", required=True)
@click.option("--output", type=click.Path(), help="Output file path")
@click.option("--model", "-m", default="facebook/musicgen-small", help="Model name")
@click.option("--duration", "-d", type=int, default=5, help="Duration in seconds")
@click.option("--temperature", "-t", type=float, default=1.0, help="Sampling temperature")
def musicgen(
    prompt: str,
    output: Optional[str],
    model: str,
    duration: int,
    temperature: float,
):
    """Generate music from text prompt using MusicGen."""
    try:
        # Parse CLI arguments into service parameters
        params = MusicGenParams(
            prompt=prompt,
            output=Path(output) if output else None,
            model=model,
            duration=duration,
            temperature=temperature,
        )
        
        # Call service
        click.echo(f"Loading model: {params.model}")
        output_path = AudiocraftService().generate_music(params)
        
        click.echo(f"✓ Generated: {output_path}")
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating music: {e}", err=True)
        sys.exit(1)


# @audiocraft_group.command()
# @click.argument("prompt", required=True)
# @click.option("--output", type=click.Path(), help="Output file path")
# @click.option("--model", "-m", default="facebook/audiogen-medium", help="Model name")
# @click.option("--duration", "-d", type=float, default=10.0, help="Duration in seconds")
# def audiogen(
#     prompt: str,
#     output: Optional[str],
#     model: str,
#     duration: float,
# ):
#     """Generate audio from text prompt using AudioGen."""
#     try:
#         # Parse CLI arguments into service parameters
#         params = AudioGenParams(
#             prompt=prompt,
#             output=Path(output) if output else None,
#             model=model,
#             duration=duration,
#         )
        
#         # Call service
#         click.echo(f"Loading model: {params.model}")
#         output_path = AudiocraftService.generate_audio(params)
        
#         click.echo(f"✓ Generated: {output_path}")
#     except ImportError as e:
#         click.echo(f"Error: {e}", err=True)
#         sys.exit(1)
#     except Exception as e:
#         click.echo(f"Error generating audio: {e}", err=True)
#         sys.exit(1)
