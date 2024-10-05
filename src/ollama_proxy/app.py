from fastapi import FastAPI
from typing import Callable
from fastapi import APIRouter

_app = None


def get_application() -> FastAPI:
    global _app
    if _app is None:
        # init application
        _app = FastAPI()
    return _app


def init_application(
    model_name: str,
    config_path: str,
    startup_event: Callable,
    router: APIRouter,
) -> FastAPI:
    global _app

    if _app is None:
        _app = FastAPI()

    _app.include_router(router)

    _app.add_event_handler("startup", startup_event)

    _app.state.config = config_path
    _app.state.model_name = model_name

    return _app
