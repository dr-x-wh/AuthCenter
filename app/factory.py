from fastapi import FastAPI

from app.api.errors import error_responses, exception_handlers
from app.api.router import router as api_router
from app.core import Settings
from app.lifespan import lifespan


def create_app(settings: Settings) -> FastAPI:
    development = settings.environment == "development"
    app = FastAPI(
        title="AuthCenter",
        openapi_url="/openapi.json" if development else None,
        lifespan=lifespan,
        exception_handlers=exception_handlers,
        responses=error_responses,
        redirect_slashes=False,
    )
    app.state.settings = settings
    app.include_router(api_router)
    return app
