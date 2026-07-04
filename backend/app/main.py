import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from app.api.v1.health import router as health_router
from app.api.v1.system import router as system_router
from app.core.config import get_settings
from app.core.exceptions import install_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import CorrelationIdMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(title="EHIS Core Foundation API", version="0.1.0")
    app.state.logger = logging.getLogger("ehis")
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    install_exception_handlers(app)
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(system_router, prefix="/api/v1")
    app.mount("/metrics", make_asgi_app())
    return app


app = create_app()
