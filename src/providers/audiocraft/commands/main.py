import click
import sys

@click.group(invoke_without_command=True)
@click.pass_context
def audiocraft_group(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        click.echo("Audiocraft requires a subcommand. Use 'musicgen'")
        sys.exit(1)
    else:
        ctx.ensure_object(dict)