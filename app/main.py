from datetime import datetime
from pathlib import Path
import json

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.schemas import ChatRequest, DispatchResponse
from app.services.dispatch_service import get_mock_alerts, handle_message
from app.services.model_service import get_model_status


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
AUDIT_FILE = BASE_DIR / "audit_logs.json"

app = FastAPI(
    title="电力通信调度智能助手",
    description="第一版演示系统，不连接真实生产系统。",
    version="0.3.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AuditRequest(BaseModel):
    session_id: str = "demo-session"
    action: str
    content: str
    operator: str = "演示调度员"


def write_audit_log(audit_request: AuditRequest) -> dict:
    """将确认记录写入本地 JSON 文件。"""
    if AUDIT_FILE.exists():
        try:
            logs = json.loads(AUDIT_FILE.read_text(encoding="utf-8"))
            if not isinstance(logs, list):
                logs = []
        except (json.JSONDecodeError, OSError):
            logs = []
    else:
        logs = []

    log_item = {
        "id": len(logs) + 1,
        "session_id": audit_request.session_id,
        "operator": audit_request.operator,
        "action": audit_request.action,
        "content": audit_request.content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    logs.append(log_item)
    AUDIT_FILE.write_text(
        json.dumps(logs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return log_item


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "power-dispatch-ai",
        "mode": "demo",
        "model": get_model_status(),
    }


@app.get("/api/config/model")
def model_config():
    """Expose non-sensitive model status for diagnostics."""
    return get_model_status()


@app.get("/api/alerts")
def alerts():
    alert_items = get_mock_alerts()
    return {"items": alert_items, "total": len(alert_items)}


@app.post("/api/dispatch/chat", response_model=DispatchResponse)
def dispatch_chat(request: ChatRequest):
    return handle_message(request.message)


@app.post("/api/audit/confirm")
def confirm_audit(request: AuditRequest):
    log_item = write_audit_log(request)
    return {"success": True, "message": "确认记录已保存。", "item": log_item}


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
