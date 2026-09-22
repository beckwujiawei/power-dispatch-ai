from __future__ import annotations

from app.skills.base import BaseSkill, SkillContext, SkillResult


class DispatchSkill(BaseSkill):
    name = "dispatch"
    description = "调度指令、调度顺序和操作建议"
    triggers = ["调度", "命令", "指令", "操作顺序", "调度建议"]
    requires_confirmation = True

    def can_handle(self, message: str) -> bool:
        return any(keyword in message for keyword in self.triggers)

    def execute(
        self,
        message: str,
        context: SkillContext,
    ) -> SkillResult:
        return SkillResult(
            skill=self.name,
            answer=(
                "调度协同能力已接入框架。当前建议先核对设备状态、告警等级和当前运行方式，"
                "再进行调度指令确认和风险评估。"
            ),
            data={
                "context": {
                    "session_id": context.session_id,
                    "operator": context.operator,
                    "message": message,
                },
                "dispatch": {
                    "status": "draft",
                    "steps": [],
                },
            },
            recommended_actions=[
                "核对设备当前运行状态",
                "确认调度指令是否符合运行方式要求",
                "确认告警/设备影响范围",
            ],
            need_confirmation=True,
        )
