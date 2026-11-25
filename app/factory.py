from fastapi import FastAPI

from app.core.errors import exception_handlers
from app.api.router import router as api_router
from app.core import Settings
from app.lifespan import lifespan


def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(lifespan=lifespan, exception_handlers=exception_handlers)
    app.state.settings = settings if settings is not None else Settings()
    app.include_router(api_router)
    return app
