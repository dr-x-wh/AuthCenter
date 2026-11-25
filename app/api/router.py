from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType

from fastapi import APIRouter

from . import routes


def _include_routes(parent: APIRouter, package: ModuleType) -> None:
    modules = iter_modules(package.__path__, prefix=f"{package.__name__}.")
    for entry in sorted(modules, key=lambda entry: entry.name):
        module = import_module(entry.name)
        if entry.ispkg:
            _include_routes(parent, module)
            continue

        feature_router = getattr(module, "router", None)
        if not isinstance(feature_router, APIRouter):
            raise TypeError(f"{entry.name} must define an APIRouter named 'router'")
        parent.include_router(feature_router)


router = APIRouter()
_include_routes(router, routes)
