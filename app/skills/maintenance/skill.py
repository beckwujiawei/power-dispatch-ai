from __future__ import annotations

from app.skills.base import BaseSkill, SkillContext, SkillResult
from app.services.report_service import build_handover_report


class HandoverReportSkill(BaseSkill):
    name = "handover_report"
    description = "生成通信调度交接班报告与待跟踪事项清单"
    triggers = ["交接班", "日报", "报告", "交班"]
    requires_confirmation = False

    def can_handle(self, message: str) -> bool:
        return any(keyword in message for keyword in self.triggers)

    def execute(
        self,
        message: str,
        context: SkillContext,
    ) -> SkillResult:
        report = build_handover_report()
        return SkillResult(
            skill=self.name,
            answer=report["summary"],
            data={
                "alerts": report.get("alerts", []),
                "tickets": report.get("tickets", []),
                "report": report,
            },
            recommended_actions=report.get("recommendations", []),
            need_confirmation=False,
        )
