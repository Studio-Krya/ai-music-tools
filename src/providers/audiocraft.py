"""Audiocraft provider - no CLI, so we implement basic use cases."""
import click
import sys
from pathlib import Path
from typing import Optional
from src.providers.base import get_default_output


@click.group(invoke_without_command=True)
@click.option("--output", type=click.Path(), help="Output file path")
@click.pass_context
def audiocraft_group(ctx: click.Context, output: Optional[str]):
    """Audiocraft audio generation (no native CLI, using Python API)."""
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
@click.option("--duration", "-d", type=float, default=10.0, help="Duration in seconds")
@click.option("--temperature", "-t", type=float, default=1.0, help="Sampling temperature")
def musicgen(prompt: str, output: Optional[str], model: str, duration: float, temperature: float):
    """Generate music from text prompt using MusicGen."""
    try:
        from audiocraft.models import MusicGen
        import torchaudio
        import torch
    except ImportError as e:
        click.echo(f"Error importing audiocraft: {e}", err=True)
        sys.exit(1)
    
    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = get_default_output("audiocraft", "wav")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        click.echo(f"Loading model: {model}")
        model_obj = MusicGen.get_pretrained(model)
        
        click.echo(f"Generating music for prompt: {prompt}")
        model_obj.set_generation_params(duration=duration, temperature=temperature)
        
        wav = model_obj.generate([prompt])
        
        click.echo(f"Saving to: {output_path}")
        torchaudio.save(str(output_path), wav[0].cpu(), model_obj.sample_rate)
        
        click.echo(f"✓ Generated: {output_path}")
    except Exception as e:
        click.echo(f"Error generating music: {e}", err=True)
        sys.exit(1)


@audiocraft_group.command()
@click.argument("prompt", required=True)
@click.option("--output", type=click.Path(), help="Output file path")
@click.option("--model", "-m", default="facebook/audiogen-medium", help="Model name")
@click.option("--duration", "-d", type=float, default=10.0, help="Duration in seconds")
def audiogen(prompt: str, output: Optional[str], model: str, duration: float):
    """Generate audio from text prompt using AudioGen."""
    try:
        from audiocraft.models import AudioGen
        import torchaudio
    except ImportError as e:
        click.echo(f"Error importing audiocraft: {e}", err=True)
        sys.exit(1)
    
    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = get_default_output("audiocraft", "wav")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        click.echo(f"Loading model: {model}")
        model_obj = AudioGen.get_pretrained(model)
        
        click.echo(f"Generating audio for prompt: {prompt}")
        model_obj.set_generation_params(duration=duration)
        
        wav = model_obj.generate([prompt])
        
        click.echo(f"Saving to: {output_path}")
        torchaudio.save(str(output_path), wav[0].cpu(), model_obj.sample_rate)
        
        click.echo(f"✓ Generated: {output_path}")
    except Exception as e:
        click.echo(f"Error generating audio: {e}", err=True)
        sys.exit(1)
