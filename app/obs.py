from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import logging
import time
from typing import Any
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def log_event(event: str, **payload: Any) -> None:
    body = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **payload,
    }
    logging.getLogger("opsboard").info(json.dumps(body, ensure_ascii=True))


@dataclass
class InMemoryMetrics:
    requests_total: int = 0
    request_latency_ms_total: float = 0
    routes: dict[str, int] = field(default_factory=dict)

    def observe(self, path: str, elapsed_ms: float) -> None:
        self.requests_total += 1
        self.request_latency_ms_total += elapsed_ms
        self.routes[path] = self.routes.get(path, 0) + 1

    @property
    def request_latency_ms_avg(self) -> float:
        if self.requests_total == 0:
            return 0
        return self.request_latency_ms_total / self.requests_total


metrics = InMemoryMetrics()


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid4()))
        request.state.request_id = request_id
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        metrics.observe(request.url.path, elapsed_ms)
        response.headers["x-request-id"] = request_id
        log_event(
            "http_request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            elapsed_ms=round(elapsed_ms, 2),
        )
        return response
