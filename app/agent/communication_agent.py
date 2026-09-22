from __future__ import annotations

from app.agent.skill_registry import SkillRegistry, build_default_registry
from app.skills.base import SkillContext, SkillResult, WorkflowStep
from app.workflows.workflow_manager import WorkflowManager

_CONFIRM_WORDS = {"确认", "确定", "继续", "ok", "yes", "同意"}


class CommunicationAgent:
    def __init__(self, registry: SkillRegistry | None = None, workflow_manager: WorkflowManager | None = None):
        self.registry = registry or build_default_registry()
        self.workflow_manager = workflow_manager or WorkflowManager()

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

        workflow_state = self.workflow_manager.get_by_session(session_id)
        if workflow_state and workflow_state.status == "waiting_for_confirmation":
            if any(word in text for word in _CONFIRM_WORDS):
                workflow_state.mark_running()
                workflow_state.add_history(
                    workflow_state.current_step or "resume",
                    {"action": "resume", "operator": operator},
                )
                return SkillResult(
                    skill="workflow_resume",
                    answer="已确认，继续执行当前任务。",
                    data={
                        "workflow_id": workflow_state.workflow_id,
                        "workflow_status": workflow_state.status,
                    },
                    need_confirmation=False,
                    confirmation_type="execution_confirm",
                )
            return SkillResult(
                skill="workflow_wait",
                answer="请确认后再继续执行当前步骤。",
                data={
                    "workflow_id": workflow_state.workflow_id,
                    "workflow_status": workflow_state.status,
                },
                need_confirmation=True,
                confirmation_type="execution_confirm",
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

        workflow = self.workflow_manager.get_by_session(session_id) or self.workflow_manager.create(session_id)
        workflow.current_step = selected.name
        workflow.mark_running()

        workflow_steps = [
            WorkflowStep(
                skill=skill.name,
                reason=skill.description,
                requires_confirmation=getattr(skill, "requires_confirmation", False),
            )
            for skill in candidates[:3]
        ]
        result.workflow_steps = workflow_steps

        if result.need_confirmation or getattr(selected, "requires_confirmation", False):
            workflow.mark_waiting_for_confirmation(selected.name)
            result.need_confirmation = True
            result.confirmation_type = "draft_review" if selected.name == "ticket_draft" else "analysis_review"
            workflow.add_history(selected.name, {"answer": result.answer, "need_confirmation": True})
        else:
            workflow.mark_completed()
            result.confirmation_type = None
            workflow.add_history(selected.name, {"answer": result.answer, "need_confirmation": False})

        result.data.setdefault("workflow_id", workflow.workflow_id)
        result.data.setdefault("workflow_status", workflow.status)
        return result
