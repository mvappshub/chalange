from __future__ import annotations

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import AuditEvent
from .metrics import http_requests_total, http_request_latency_seconds

class MetricsAndAuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        response = await call_next(request)

        path = request.url.path
        method = request.method
        status = str(response.status_code)
        http_requests_total.labels(method=method, path=path, status=status).inc()
        http_request_latency_seconds.labels(method=method, path=path).observe(time.time() - start)

        # Lightweight request audit
        try:
            db: Session = SessionLocal()
            ae = AuditEvent(
                actor="anonymous",
                action="http_request",
                entity_type="http",
                entity_id=f"{method} {path}",
                correlation_id=correlation_id,
                details_json=f'{{"status": {response.status_code}}}',
            )
            db.add(ae)
            db.commit()
        finally:
            db.close()

        response.headers["x-correlation-id"] = correlation_id
        return response
