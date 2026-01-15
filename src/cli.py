"""Main CLI entry point."""
from pathlib import Path
import click
import uuid
from src.providers.audiocraft import audiocraft_group
from src.providers.audiocraft.service import AudiocraftService
from src.providers.base import get_default_output, run_command

DEFAULT_TEXT = "Hello, world! this is a sample"
DEFAULT_PROMPT = "lo-fi music with a soothing melody"

MODELS = {
    'audiocraft': ["facebook/musicgen-small", "facebook/musicgen-large"],
    'audioldm': ["audioldm-s-full"],
    'tts': ["tts_models/pt/cv/vits"],
}

def slugify(text: str) -> str:
    return text.lower().replace("/", "-")

@click.group()
def cli():
    """AI Music Models CLI - Unified interface for audio generation tools."""
    pass

@click.command()
def initialize():

    print("Installing models...")

    # iterate over MODELS keys and values
    for model, values in MODELS.items():
        for value in values:
            output_path = str(get_default_output("init", f"{model}_{slugify(value)}_{uuid.uuid4()}.wav"))  
            output_resolved = str(Path(output_path).resolve())
            
            print(f"Installing {model} => {value}")

            if model == 'audiocraft':
                service = AudiocraftService()
                service.initialize_model(value)
                service.unload_model(value)
                continue
            if model == 'audioldm':
                args = ["uv", "run", "audioldm", "-t", f'"{DEFAULT_TEXT}"', "--model_name", value, "-s", output_resolved]
                run_command(args, raw_cli=True)
                continue
            if model == 'tts':
                run_command(["uv", "run", "tts", "--text", f'"{DEFAULT_TEXT}"', "--out_path", output_path], raw_cli=True)
                continue
            # run_command([f"uv run {model} --download {value}"], raw_cli=True)

        # Should always generate with the default model CoquiTTS
        if model == 'tts':
            print("Installing default TTS model...")
            output_path = get_default_output("init", f"tts_default_{uuid.uuid4()}.wav")    
            run_command(["uv", "run", "tts", "--text", f'"{DEFAULT_TEXT}"', "--out_path", output_path], raw_cli=True)
            pass
            # 

    # run_command(["uv", "--version"], raw_cli=True)
    """Initialize the CLI."""
    pass


cli.add_command(audiocraft_group, name="audiocraft")
cli.add_command(initialize, name="initialize")

if __name__ == "__main__":
    cli()

