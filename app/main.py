from datetime import datetime
from pathlib import Path
import json

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.schemas import ChatRequest, DispatchResponse
from app.services.dispatch_service import get_mock_alerts, handle_message
from app.services.model_service import get_model_status
from app.services.report_service import build_handover_report
from app.services.ticket_service import (
    VALID_STATUSES,
    create_ticket,
    list_tickets,
    update_ticket_status,
)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
AUDIT_FILE = BASE_DIR / "audit_logs.json"

app = FastAPI(title="电力通信调度智能助手", description="第一版演示系统，不连接真实生产系统。", version="0.6.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AuditRequest(BaseModel):
    session_id: str = "demo-session"
    action: str
    content: str
    operator: str = "演示调度员"


class TicketCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    priority: str = "一般"
    station: str = ""
    related_device: str = ""
    description: str = ""
    operator: str = "演示调度员"
    session_id: str = "demo-session"


class TicketStatusRequest(BaseModel):
    status: str
    operator: str = "演示调度员"
    session_id: str = "demo-session"


def write_audit_log(audit_request: AuditRequest) -> dict:
    try:
        logs = json.loads(AUDIT_FILE.read_text(encoding="utf-8")) if AUDIT_FILE.exists() else []
        if not isinstance(logs, list):
            logs = []
    except (json.JSONDecodeError, OSError):
        logs = []
    log_item = {"id": len(logs) + 1, "session_id": audit_request.session_id, "operator": audit_request.operator, "action": audit_request.action, "content": audit_request.content, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    logs.append(log_item)
    AUDIT_FILE.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")
    return log_item


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "power-dispatch-ai", "mode": "demo", "model": get_model_status()}


@app.get("/api/config/model")
def model_config():
    return get_model_status()


@app.get("/api/alerts")
def alerts(station: str | None = Query(default=None), level: str | None = Query(default=None), status: str | None = Query(default=None)):
    items = get_mock_alerts()
    if station:
        items = [item for item in items if item.station == station]
    if level:
        items = [item for item in items if item.level == level]
    if status:
        items = [item for item in items if item.status == status]
    return {"items": items, "total": len(items), "filters": {"station": station, "level": level, "status": status}}


@app.post("/api/dispatch/chat", response_model=DispatchResponse)
def dispatch_chat(request: ChatRequest):
    return handle_message(request.message)


@app.get("/api/reports/handover")
def handover_report():
    return build_handover_report()


@app.post("/api/audit/confirm")
def confirm_audit(request: AuditRequest):
    return {"success": True, "message": "确认记录已保存。", "item": write_audit_log(request)}


@app.get("/api/audit/logs")
def get_audit_logs():
    if not AUDIT_FILE.exists():
        return {"items": [], "total": 0}
    try:
        logs = json.loads(AUDIT_FILE.read_text(encoding="utf-8"))
        if not isinstance(logs, list):
            logs = []
    except (json.JSONDecodeError, OSError):
        logs = []
    return {"items": logs, "total": len(logs)}


@app.post("/api/tickets")
def create_ticket_endpoint(request: TicketCreateRequest):
    ticket = create_ticket(request.model_dump(exclude={"operator", "session_id"}), request.operator)
    write_audit_log(AuditRequest(session_id=request.session_id, operator=request.operator, action="确认并创建工单", content=f"工单 {ticket['id']}：{ticket['title']}"))
    return {"success": True, "message": "工单已创建。", "item": ticket}


@app.get("/api/tickets")
def get_tickets(status: str | None = Query(default=None)):
    if status and status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"不支持的工单状态：{status}")
    items = list_tickets(status)
    return {"items": items, "total": len(items), "statuses": sorted(VALID_STATUSES)}


@app.patch("/api/tickets/{ticket_id}/status")
def change_ticket_status(ticket_id: str, request: TicketStatusRequest):
    try:
        ticket = update_ticket_status(ticket_id, request.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if ticket is None:
        raise HTTPException(status_code=404, detail="工单不存在")
    write_audit_log(AuditRequest(session_id=request.session_id, operator=request.operator, action="更新工单状态", content=f"工单 {ticket_id} 状态更新为：{request.status}"))
    return {"success": True, "message": "工单状态已更新。", "item": ticket}
