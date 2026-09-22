from __future__ import annotations

from app.skills.base import BaseSkill, SkillContext, SkillResult
from app.services.dispatch_service import analyze_alerts


class AlertAnalysisSkill(BaseSkill):
    name = "alert_analysis"
    description = "分析通信告警、判断可能原因并给出排查建议"
    triggers = ["告警", "故障", "异常", "中断", "分析"]

    def can_handle(self, message: str) -> bool:
        return any(keyword in message for keyword in self.triggers)

    def execute(
        self,
        message: str,
        context: SkillContext,
    ) -> SkillResult:
        response = analyze_alerts()
        return SkillResult(
            skill=self.name,
            answer=response.answer,
            data={"alerts": [alert.model_dump() for alert in response.alerts]},
            recommended_actions=response.recommended_actions,
            need_confirmation=response.need_confirmation,
        )
