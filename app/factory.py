from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core import get_settings
from app.lifespan import lifespan


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.app_debug, lifespan=lifespan)
    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(auth_router)
    return app
