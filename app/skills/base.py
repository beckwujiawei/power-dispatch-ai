from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WorkflowStep:
    def __init__(
        self,
        *,
        skill: str,
        reason: str = "",
        requires_confirmation: bool = False,
    ):
        self.skill = skill
        self.reason = reason
        self.requires_confirmation = requires_confirmation

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill": self.skill,
            "reason": self.reason,
            "requires_confirmation": self.requires_confirmation,
        }


class SkillContext:
    def __init__(
        self,
        *,
        session_id: str,
        operator: str = "演示调度员",
        metadata: dict[str, Any] | None = None,
    ):
        self.session_id = session_id
        self.operator = operator
        self.metadata = metadata or {}


class SkillResult:
    def __init__(
        self,
        *,
        skill: str,
        answer: str,
        data: dict[str, Any] | None = None,
        recommended_actions: list[str] | None = None,
        need_confirmation: bool = False,
        workflow_steps: list[WorkflowStep] | None = None,
        confirmation_type: str | None = None,
    ):
        self.skill = skill
        self.answer = answer
        self.data = data or {}
        self.recommended_actions = recommended_actions or []
        self.need_confirmation = need_confirmation
        self.workflow_steps = workflow_steps or []
        self.confirmation_type = confirmation_type

    def to_dispatch_response(self):
        from app.schemas import Alert, DispatchResponse

        raw_alerts = self.data.get("alerts", [])
        alert_list = []
        for alert in raw_alerts:
            if isinstance(alert, Alert):
                alert_list.append(alert)
            elif isinstance(alert, dict):
                alert_list.append(Alert(**alert))

        ticket_draft = self.data.get("ticket_draft")
        workflow = [step.to_dict() for step in self.workflow_steps]
        return DispatchResponse(
            intent=self.skill,
            answer=self.answer,
            alerts=alert_list,
            recommended_actions=self.recommended_actions,
            ticket_draft=ticket_draft,
            need_confirmation=self.need_confirmation,
            workflow=workflow,
            confirmation_type=self.confirmation_type,
        )


class BaseSkill(ABC):
    name: str = ""
    description: str = ""
    triggers: list[str] = []
    requires_confirmation: bool = False

    @abstractmethod
    def can_handle(self, message: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        message: str,
        context: SkillContext,
    ) -> SkillResult:
        raise NotImplementedError
