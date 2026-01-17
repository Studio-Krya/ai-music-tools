import click
import uuid

from src.utils.file import get_folder_output
from src.utils.shell import run_command_quiet

@click.command()
@click.argument("text", required=True)
@click.option("--model", "-m", default="tts_models/pt/cv/vits", help="Model to use")
@click.option("--output", "-o", help="Output file")
def tts(text: str, model: str, output: str):
    output_path = output or get_folder_output("tts")

    coqui_args = {
        "--text": text,
        "--model_name": model,
        "--output_path": output_path,
    }

    args = [coqui_args.keys(), coqui_args.values()]
    print(args)
    # srun_command(["uv", "run", "tts", args])