from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field

from .models import Severity, IncidentStatus

class CardCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    list_id: int

class CardMove(BaseModel):
    list_id: int

class IncidentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    severity: Severity = Severity.medium

class IncidentEventCreate(BaseModel):
    kind: str = Field(default="note", max_length=100)
    message: str = Field(min_length=1)

class AlertCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    severity: Severity = Severity.medium
    source: str = "manual"
    message: str | None = None

class AuditOut(BaseModel):
    id: int
    at: datetime
    actor: str
    action: str
    entity_type: str
    entity_id: str
    correlation_id: str | None
    details_json: str | None

    class Config:
        from_attributes = True
