from datetime import datetime
import json
from pathlib import Path
from typing import Any
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent.parent.parent
TICKET_FILE = BASE_DIR / "tickets.json"

VALID_STATUSES = {"待确认", "已确认", "处理中", "已关闭"}


def _read_tickets() -> list[dict[str, Any]]:
    if not TICKET_FILE.exists():
        return []
    try:
        data = json.loads(TICKET_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def _write_tickets(tickets: list[dict[str, Any]]) -> None:
    TICKET_FILE.write_text(
        json.dumps(tickets, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def create_ticket(draft: dict[str, Any], operator: str) -> dict[str, Any]:
    tickets = _read_tickets()
    ticket = {
        "id": f"TICKET-{datetime.now():%Y%m%d}-{uuid4().hex[:6].upper()}",
        "title": draft.get("title", "通信故障工单"),
        "priority": draft.get("priority", "一般"),
        "station": draft.get("station", ""),
        "related_device": draft.get("related_device", ""),
        "description": draft.get("description", ""),
        "status": "已确认",
        "operator": operator,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tickets.append(ticket)
    _write_tickets(tickets)
    return ticket


def list_tickets(status: str | None = None) -> list[dict[str, Any]]:
    tickets = _read_tickets()
    if status:
        tickets = [ticket for ticket in tickets if ticket.get("status") == status]
    return list(reversed(tickets))


def update_ticket_status(ticket_id: str, status: str) -> dict[str, Any] | None:
    if status not in VALID_STATUSES:
        raise ValueError(f"不支持的工单状态：{status}")
    tickets = _read_tickets()
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            ticket["status"] = status
            ticket["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _write_tickets(tickets)
            return ticket
    return None
