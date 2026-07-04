from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "service": get_settings().service_name}


@router.get("/readyz")
async def readyz() -> dict[str, str]:
    return {"status": "ready"}
