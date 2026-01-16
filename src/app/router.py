from .tracks.router import router as tracks_router
from fastapi.routing import APIRouter

router = APIRouter()

router.include_router(tracks_router)