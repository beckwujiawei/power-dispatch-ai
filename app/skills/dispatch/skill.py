from __future__ import annotations

from app.skills.base import BaseSkill, SkillContext, SkillResult


class MaintenanceSkill(BaseSkill):
    name = "maintenance"
    description = "检修计划、检修任务和检修清单管理"
    triggers = ["检修", "维修", "检修计划", "检修任务", "停电", "停送电"]
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
                "检修管理能力已接入框架，当前为示例实现。"
                "建议先确认检修对象、检修方式、停电范围和安全措施，再生成作业计划。"
            ),
            data={
                "context": {
                    "session_id": context.session_id,
                    "operator": context.operator,
                    "message": message,
                },
                "maintenance": {
                    "status": "draft",
                    "tasks": [],
                },
            },
            recommended_actions=[
                "确认检修设备与停电范围",
                "确认安全措施和工作票要求",
                "确认检修窗口与回送时间",
            ],
            need_confirmation=True,
        )
