from fastapi import FastAPI

from .health import api as health_api
from .auth import api as auth_api

routers = [health_api, auth_api]


def init_api(app: FastAPI) -> None:
    for api in routers:
        app.include_router(api)
