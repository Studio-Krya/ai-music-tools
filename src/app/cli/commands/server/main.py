import click
import asyncio

from src.app.workers.track_processor import TrackProcessor
from src.core.database import async_get_db
from src.utils.shell import run_command

@click.group(invoke_without_command=True)
@click.pass_context
def server_group(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        run_command(["uv", "run", "uvicorn", "src.api:app", "--reload"])
    else:
        ctx.ensure_object(dict)

@server_group.command()
@click.argument("queue_name", type=str)
def ingest_queue(queue_name: str):
    async def run():
        async for db in async_get_db():
            queue = TrackProcessor(db).queue
            queue.put({"track_id": "66c10999-32a5-4bc3-81a7-e26afbe6c513", "job_id": "cfa5ded7-889d-47c1-9aeb-ce5854f01c2b"})
            print(f"✓ Ingested queue: {queue_name}")

    asyncio.run(run())

@server_group.command()
@click.argument("queue_name", type=str)
def peak_queue(queue_name: str):
    async def run():
        async for db in async_get_db():
            queue = TrackProcessor(db).queue
            print(f"✓ Peeked queue: {queue_name}")
            print(queue.peek())

    asyncio.run(run())