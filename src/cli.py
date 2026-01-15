"""Main CLI entry point."""
import click
from src.providers.audiocraft import audiocraft_group


@click.group()
def cli():
    """AI Music Models CLI - Unified interface for audio generation tools."""
    pass


@cli.group()
def generate():
    """Generate audio using various providers."""
    pass


generate.add_command(audiocraft_group, name="audiocraft")

if __name__ == "__main__":
    cli()
