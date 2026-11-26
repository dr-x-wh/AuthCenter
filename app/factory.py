from fastapi import FastAPI

from app.api.router import router as api_router
from app.core import settings
from app.core.errors import exception_handlers
from app.core.logging import configure_logging
from app.lifespan import lifespan


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    app = FastAPI(lifespan=lifespan, exception_handlers=exception_handlers)
    app.state.settings = settings
    app.include_router(api_router)
    return app
