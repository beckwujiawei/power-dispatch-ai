from __future__ import annotations

from app.agent.skill_registry import SkillRegistry, build_default_registry
from app.skills.base import SkillContext, SkillResult, WorkflowStep


class CommunicationAgent:
    def __init__(self, registry: SkillRegistry | None = None):
        self.registry = registry or build_default_registry()

    def handle(
        self,
        message: str,
        *,
        session_id: str = "demo-session",
        operator: str = "演示调度员",
    ) -> SkillResult:
        text = message.strip()
        if not text:
            return SkillResult(
                skill="unknown",
                answer="请告诉我需要查询或处理什么内容。",
            )

        candidates = self.registry.find_by_message(text)
        if not candidates:
            return SkillResult(
                skill="general",
                answer=(
                    "我是通信调度智能助手，可以帮助你处理告警分析、检修、调度、"
                    "运行方式、工单和交接班报告。"
                ),
            )

        context = SkillContext(session_id=session_id, operator=operator)
        selected = candidates[0]
        result = selected.execute(text, context)

        if len(candidates) > 1:
            workflow_steps = [
                WorkflowStep(
                    skill=skill.name,
                    reason=skill.description,
                    requires_confirmation=getattr(skill, "requires_confirmation", False),
                )
                for skill in candidates[:3]
            ]
            result.workflow_steps = workflow_steps
            result.confirmation_type = "analysis_review" if len(workflow_steps) > 1 else "draft_review"
            result.need_confirmation = True

        return result
