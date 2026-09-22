from __future__ import annotations

from app.skills.base import BaseSkill, SkillContext, SkillResult


class OperationModeSkill(BaseSkill):
    name = "operation_mode"
    description = "运行方式分析、方式切换建议和风险提示"
    triggers = ["运行方式", "方式切换", "备用", "运行模式", "倒换"]

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
                "运行方式能力已接入框架。当前建议优先检查现有方式状态、备用链路状态和故障影响范围，"
                "确认切换方案是否满足安全和业务连续性要求。"
            ),
            data={
                "context": {
                    "session_id": context.session_id,
                    "operator": context.operator,
                    "message": message,
                },
                "operation_mode": {
                    "status": "analysis",
                    "mode": "current",
                    "warnings": [],
                },
            },
            recommended_actions=[
                "确认当前运行方式和备用方式状态",
                "评估切换对业务的影响范围",
                "确认倒换前后的安全措施",
            ],
            need_confirmation=True,
        )
