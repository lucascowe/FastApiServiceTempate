import logging
import time
from contextvars import ContextVar

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


ctx = ContextVar("request_context")


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"Before {request.method} {request.url} {call_next}")
        request.state.start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - request.state.start_time
        logger.info(f"After {request.method} {request.url} {response.status_code} in {round(process_time, 3)}s")
        response.headers["X-Process-Time"] = str(process_time)
        return response


def add_middleware(app: FastAPI):
    app.add_middleware(CustomMiddleware)