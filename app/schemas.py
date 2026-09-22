from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "demo-session"


class WorkflowStep(BaseModel):
    skill: str
    reason: str = ""
    requires_confirmation: bool = False


class Alert(BaseModel):
    id: str
    station: str
    device: str
    alert_type: str
    level: str
    status: str
    occurred_at: str
    description: str


class DispatchResponse(BaseModel):
    intent: str
    answer: str
    alerts: list[Alert] = []
    recommended_actions: list[str] = []
    ticket_draft: Optional[dict] = None
    need_confirmation: bool = False
    workflow: list[WorkflowStep] = []
    confirmation_type: Optional[str] = None
