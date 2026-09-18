from datetime import datetime
from typing import List

from app.schemas import Alert, DispatchResponse


MOCK_ALERTS = [
    Alert(
        id="ALERT-20260917-001",
        station="华东变电站",
        device="2号传输设备",
        alert_type="设备离线",
        level="严重",
        status="未恢复",
        occurred_at="2026-09-17 10:20:15",
        description="传输设备管理通道中断，设备无法正常通信。",
    ),
    Alert(
        id="ALERT-20260917-002",
        station="华东变电站",
        device="主用光纤链路",
        alert_type="链路中断",
        level="严重",
        status="未恢复",
        occurred_at="2026-09-17 10:20:18",
        description="主用光纤链路出现中断告警。",
    ),
    Alert(
        id="ALERT-20260917-003",
        station="华南变电站",
        device="调度自动化通道",
        alert_type="业务中断",
        level="重要",
        status="未恢复",
        occurred_at="2026-09-17 10:21:02",
        description="调度自动化远动业务通信异常。",
    ),
]


def get_mock_alerts() -> List[Alert]:
    return MOCK_ALERTS


def analyze_alerts() -> DispatchResponse:
    return DispatchResponse(
        intent="alert_analysis",
        answer=(
            "根据当前模拟数据，华东变电站在 10:20 左右出现传输设备离线和主用光纤链路中断。"
            "初步判断可能存在传输设备故障、光纤链路故障或站点通信电源异常。"
            "目前结论仅供辅助分析，需要调度人员进一步核查。"
        ),
        alerts=MOCK_ALERTS,
        recommended_actions=[
            "核查华东变电站通信电源及传输设备运行状态。",
            "核查主用光纤链路两端设备和光功率。",
            "确认备用通信链路是否正常承载业务。",
            "确认调度自动化远动业务是否受到影响。",
            "必要时联系现场通信运维人员进行人工检查。",
        ],
        need_confirmation=True,
    )


def create_ticket_draft() -> DispatchResponse:
    ticket = {
        "title": "华东变电站通信链路异常",
        "priority": "高",
        "station": "华东变电站",
        "related_device": "2号传输设备",
        "description": (
            "华东变电站出现传输设备离线和主用光纤链路中断告警，"
            "疑似影响调度自动化远动业务，需进一步核查。"
        ),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "待人工确认",
    }

    return DispatchResponse(
        intent="ticket_draft",
        answer="已生成故障工单草稿，但尚未提交到真实工单系统。",
        alerts=MOCK_ALERTS,
        ticket_draft=ticket,
        need_confirmation=True,
    )


def handle_message(message: str) -> DispatchResponse:
    text = message.strip()

    if not text:
        return DispatchResponse(
            intent="unknown",
            answer="请告诉我需要查询或处理什么内容。",
        )

    if any(keyword in text for keyword in ["告警", "故障", "异常", "中断", "分析"]):
        return analyze_alerts()

    if any(keyword in text for keyword in ["工单", "报修", "创建任务"]):
        return create_ticket_draft()

    if any(keyword in text for keyword in ["交接班", "日报", "报告"]):
        return DispatchResponse(
            intent="report",
            answer=(
                "当前可以生成通信调度日报。今日模拟数据中发现 3 条未恢复告警，"
                "其中 2 条为严重告警，建议优先处理华东变电站通信异常。"
            ),
            alerts=MOCK_ALERTS,
            recommended_actions=[
                "跟踪华东变电站故障处理进度。",
                "确认调度自动化业务是否已恢复。",
                "在交接班记录中标注未恢复告警。",
            ],
        )

    if any(keyword in text for keyword in ["查询", "查看", "有哪些"]):
        return DispatchResponse(
            intent="alert_query",
            answer=f"当前共有 {len(MOCK_ALERTS)} 条模拟通信告警，其中 {sum(1 for x in MOCK_ALERTS if x.status == '未恢复')} 条尚未恢复。",
            alerts=MOCK_ALERTS,
        )

    return DispatchResponse(
        intent="general_question",
        answer=(
            "我是电力通信调度智能助手。目前可以帮助你查询通信告警、"
            "分析通信故障、生成工单草稿和整理交接班信息。"
        ),
        recommended_actions=[
            "例如：分析当前通信告警",
            "例如：查询有哪些未恢复告警",
            "例如：生成一个故障工单",
            "例如：生成交接班报告",
        ],
    )