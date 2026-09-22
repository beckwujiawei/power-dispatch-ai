from __future__ import annotations

from app.skills.alert_analysis.skill import AlertAnalysisSkill
from app.skills.base import BaseSkill
from app.skills.dispatch.skill import DispatchSkill
from app.skills.handover_report.skill import HandoverReportSkill
from app.skills.maintenance.skill import MaintenanceSkill
from app.skills.operation_mode.skill import OperationModeSkill
from app.skills.ticket.skill import TicketDraftSkill


class SkillRegistry:
    def __init__(self):
        self._skills: dict[str, BaseSkill] = {}

    def register(self, skill: BaseSkill) -> None:
        self._skills[skill.name] = skill

    def get(self, name: str) -> BaseSkill | None:
        return self._skills.get(name)

    def all(self) -> list[BaseSkill]:
        return list(self._skills.values())

    def find_by_message(self, message: str) -> list[BaseSkill]:
        text = message.strip()
        if not text:
            return []
        return [skill for skill in self._skills.values() if skill.can_handle(text)]


def build_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    registry.register(AlertAnalysisSkill())
    registry.register(TicketDraftSkill())
    registry.register(HandoverReportSkill())
    registry.register(MaintenanceSkill())
    registry.register(DispatchSkill())
    registry.register(OperationModeSkill())
    return registry
