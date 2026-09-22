from __future__ import annotations

from app.skills.base import BaseSkill, SkillContext, SkillResult
from app.services.dispatch_service import create_ticket_draft


class TicketDraftSkill(BaseSkill):
    name = "ticket_draft"
    description = "生成故障工单草稿，供调度员审核后提交"
    triggers = ["工单", "报修", "创建任务", "故障工单"]
    requires_confirmation = True

    def can_handle(self, message: str) -> bool:
        return any(keyword in message for keyword in self.triggers)

    def execute(
        self,
        message: str,
        context: SkillContext,
    ) -> SkillResult:
        response = create_ticket_draft()
        return SkillResult(
            skill=self.name,
            answer=response.answer,
            data={
                "alerts": [alert.model_dump() for alert in response.alerts],
                "ticket_draft": response.ticket_draft,
            },
            recommended_actions=response.recommended_actions,
            need_confirmation=response.need_confirmation,
        )
