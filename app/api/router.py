from fastapi import APIRouter

from .routes import routers

router = APIRouter()
for feature_router in routers:
    router.include_router(feature_router)
