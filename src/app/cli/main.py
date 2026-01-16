import click

from src.providers.audiocraft.commands import audiocraft_group
from src.app.cli.commands.initialize import initialize
from src.app.cli.commands.server import server_group

@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Version of the application")
def cli(version: bool):
    if(version):
        print(f"Krya CLI Version: 1.0.0")
        return   


# All commands registry
cli.add_command(initialize, name="initialize")
cli.add_command(audiocraft_group, name="audiocraft")
cli.add_command(server_group, name="server")
