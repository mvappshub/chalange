from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .db import engine, Base, SessionLocal
from .middleware import MetricsAndAuditMiddleware
from .routers.api import router as api_router
from .routers.ui import router as ui_router
from .routers.ops import router as ops_router
from .services import ensure_seed

app = FastAPI(title="OpsBoard MVP", version="0.1.0")

app.add_middleware(MetricsAndAuditMiddleware)
app.include_router(ops_router)
app.include_router(api_router)
app.include_router(ui_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def _startup():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        ensure_seed(db)
    finally:
        db.close()
