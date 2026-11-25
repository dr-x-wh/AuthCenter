from fastapi import FastAPI

from app import api
from app import logger
from app.lifespan import lifespan

logger.init()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    api.init_api(app)
    return app
