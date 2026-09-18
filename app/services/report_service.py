from datetime import datetime
import json
from pathlib import Path
from typing import Any

from app.services.dispatch_service import get_mock_alerts
from app.services.ticket_service import list_tickets


REPORT_DIR = Path(__file__).resolve().parent.parent.parent


def build_handover_report() -> dict[str, Any]:
    alerts = get_mock_alerts()
    tickets = list_tickets()
    unresolved_alerts = [alert for alert in alerts if alert.status != "已恢复"]
    severe_alerts = [alert for alert in unresolved_alerts if alert.level == "严重"]
    open_tickets = [ticket for ticket in tickets if ticket.get("status") != "已关闭"]

    recommendations = []
    if severe_alerts:
        recommendations.append(f"优先跟踪 {len(severe_alerts)} 条严重告警，重点关注：{severe_alerts[0].station}。")
    if open_tickets:
        recommendations.append(f"继续跟踪 {len(open_tickets)} 条未关闭工单的处理进度。")
    recommendations.extend([
        "交接前确认通信链路和调度自动化业务恢复情况。",
        "将未恢复告警和现场核查结果补充到值班记录。",
    ])

    return {
        "title": "电力通信调度交接班报告",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": f"当前有 {len(unresolved_alerts)} 条未恢复告警，其中严重告警 {len(severe_alerts)} 条；未关闭工单 {len(open_tickets)} 条。",
        "statistics": {
            "total_alerts": len(alerts),
            "unresolved_alerts": len(unresolved_alerts),
            "severe_alerts": len(severe_alerts),
            "open_tickets": len(open_tickets),
        },
        "alerts": [alert.model_dump() for alert in unresolved_alerts],
        "tickets": open_tickets,
        "recommendations": recommendations,
    }
