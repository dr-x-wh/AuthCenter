from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core import Settings
from app.lifespan import lifespan


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.environment == "development",
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(auth_router)
    return app
