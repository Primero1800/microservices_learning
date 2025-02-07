from typing import Callable, Any

from fastapi import APIRouter
from starlette.applications import Starlette
from .routing import APIRouter
from starlette.types import Scope, Receive, Send


class FastApi(Starlette):
    def __init__(self, version: str = "0.1.0") -> None:
        # super().__init__()
        self.version = version
        self.router: APIRouter = APIRouter()

    def get(self, path: str) -> Callable[..., Any]:
        return self.router.get(path)

    def post(self, path: str) -> Callable[..., Any]:
            return self.router.post(path)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await super().__call__(scope, receive, send)