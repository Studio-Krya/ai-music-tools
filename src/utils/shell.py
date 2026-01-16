from typing import List, Optional
import subprocess
import sys

def run_command(
    command: List[str],
    additional_args: Optional[List[str]] = None,
) -> int:
    if additional_args:
        command.extend(additional_args)

    try:
        result = subprocess.run(command, check=True)
        return result.returncode
    except Exception as e:
        print(f"Error running command: {e}", file=sys.stderr)
        return 1

def run_command_quiet(
    command: List[str],
    additional_args: Optional[List[str]] = None,
) -> int:
    if additional_args:
        command.extend(additional_args)

    try:
        result = subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode
    except Exception as e:
        print(f"Error running command: {e}", file=sys.stderr)
        return 1