from typing import List, Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "demo-session"


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
    alerts: List[Alert] = []
    recommended_actions: List[str] = []
    ticket_draft: Optional[dict] = None
    need_confirmation: bool = False