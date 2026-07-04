import time
from uuid import uuid4
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.correlation_id = request.headers.get("x-correlation-id", str(uuid4()))
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["x-correlation-id"] = request.state.correlation_id
        response.headers["x-response-time-ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
        return response
