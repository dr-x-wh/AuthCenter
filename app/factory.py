from fastapi import FastAPI

from app.api.router import router as api_router
from app.core import Settings
from app.lifespan import lifespan


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.environment == "development",
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.include_router(api_router)
    return app
