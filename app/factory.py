from fastapi import FastAPI

from app.api.router import router as api_router
from app.core import Settings
from app.core.errors import exception_handlers
from app.core.logging import configure_logging
from app.lifespan import lifespan


def create_app(settings: Settings | None = Settings()) -> FastAPI:
    configure_logging(settings.log_level)
    app = FastAPI(lifespan=lifespan, exception_handlers=exception_handlers)
    app.state.settings = settings
    app.include_router(api_router)
    return app
