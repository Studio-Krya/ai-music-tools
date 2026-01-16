import click
import uuid
from pathlib import Path

from src.constants import BASE_MODEL_MAP
from src.utils.file import get_folder_output
from src.utils.shell import run_command_quiet
from src.providers.audiocraft.service import AudiocraftService

DEFAULT_TEXT = "Hello, world! this is a sample"

@click.command()
def initialize():
    for model, values in BASE_MODEL_MAP.items():
        for value in values:
            output_path = str(get_folder_output("init", f"{model}_{slugify(value)}_{uuid.uuid4()}.wav"))  
            output_resolved = str(Path(output_path).resolve())
            
            print(f"Installing {model} => {value}")

            if model == 'audiocraft':
                service = AudiocraftService() 
                service.initialize_model(value)
                service.unload_model(value)
                continue
            if model == 'audioldm':
                args = ["uv", "run", "audioldm", "-t", f'"{DEFAULT_TEXT}"', "--model_name", value, "-s", output_resolved]
                run_command_quiet(args, raw_cli=True)
                continue
            if model == 'tts':
                run_command_quiet(["uv", "run", "tts", "--text", f'"{DEFAULT_TEXT}"', "--out_path", output_path], raw_cli=True)
                continue

        if model == 'tts':
            output_path = get_folder_output("init", f"tts_default_{uuid.uuid4()}.wav")    
            run_command_quiet(["uv", "run", "tts", "--text", f'"{DEFAULT_TEXT}"', "--out_path", output_path], raw_cli=True)

def slugify(text: str) -> str:
    return text.lower().replace("/", "-")