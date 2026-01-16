from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator, Callable
from sqlmodel import SQLModel
import anyio
import asyncio
from src.app.workers.main import listen

from .database import async_engine, async_get_db

async def set_threadpool_tokens(number_of_tokens: int = 100) -> None:
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = number_of_tokens


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI, create_tables_on_start: bool = True) -> AsyncGenerator:
    stop = asyncio.Event()

    await create_db_and_tables()

    async for db in async_get_db():
        task = asyncio.create_task(listen(db, stop))

    yield

    stop.set()
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)

    # if isinstance(settings, DatabaseSettings) and create_tables_on_start:
    #     await create_tables()

    # if settings.ENVIRONMENT != EnvironmentOption.LOCAL:
    #     if isinstance(settings, RedisCacheSettings):
    #         await create_redis_cache_pool()

    #     if isinstance(settings, RedisQueueSettings):
    #         await create_redis_queue_pool()

    #     if isinstance(settings, RedisRateLimiterSettings):
    #         await create_redis_rate_limit_pool()

    # yield

    # if isinstance(settings, RedisCacheSettings):
    #     await close_redis_cache_pool()

    # if isinstance(settings, RedisQueueSettings):
    #     await close_redis_queue_pool()

    # if isinstance(settings, RedisRateLimiterSettings):
    #     await close_redis_rate_limit_pool()

def create_application(
    router: APIRouter,
    **kwargs: Any,
) -> FastAPI:
    application = FastAPI(lifespan=lifespan, **kwargs)
    application.include_router(router)

    # CORS

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.mount(
        "/storage",
        StaticFiles(directory="storage"),
        name="storage",
    )

    return application

    # if isinstance(settings, AppSettings):
    #     to_update = {
    #         "title": settings.APP_NAME,
    #         "description": settings.APP_DESCRIPTION,
    #         "contact": {"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
    #         "license_info": {"name": settings.LICENSE_NAME},
    #     }
    #     kwargs.update(to_update)

    # if isinstance(settings, EnvironmentSettings):
    #     kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    # lifespan = lifespan_factory(settings, create_tables_on_start=create_tables_on_start)

    # application = FastAPI(lifespan=lifespan, **kwargs)
    # application.include_router(router)

    # if isinstance(settings, ClientSideCacheSettings):
    #     application.add_middleware(ClientCacheMiddleware, max_age=settings.CLIENT_CACHE_MAX_AGE)

    # if isinstance(settings, EnvironmentSettings):
    #     if settings.ENVIRONMENT != EnvironmentOption.PRODUCTION:
    #         docs_router = APIRouter()
    #         if settings.ENVIRONMENT != EnvironmentOption.LOCAL:
    #             docs_router = APIRouter(dependencies=[Depends(get_current_superuser)])

    #         @docs_router.get("/docs", include_in_schema=False)
    #         async def get_swagger_documentation() -> fastapi.responses.HTMLResponse:
    #             return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

    #         @docs_router.get("/redoc", include_in_schema=False)
    #         async def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
    #             return get_redoc_html(openapi_url="/openapi.json", title="docs")

    #         @docs_router.get("/openapi.json", include_in_schema=False)
    #         async def openapi() -> dict[str, Any]:
    #             out: dict = get_openapi(title=application.title, version=application.version, routes=application.routes)
    #             return out

    #         application.include_router(docs_router)

    #     return application