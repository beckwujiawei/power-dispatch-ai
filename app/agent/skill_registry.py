from __future__ import annotations

from app.agent.skill_registry import SkillRegistry
from app.skills.dispatch.skill import DispatchSkill
from app.skills.maintenance.skill import MaintenanceSkill
from app.skills.operation_mode.skill import OperationModeSkill


def build_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    from app.skills.alert_analysis.skill import AlertAnalysisSkill
    from app.skills.handover_report.skill import HandoverReportSkill
    from app.skills.ticket.skill import TicketDraftSkill

    registry.register(AlertAnalysisSkill())
    registry.register(TicketDraftSkill())
    registry.register(HandoverReportSkill())
    registry.register(MaintenanceSkill())
    registry.register(DispatchSkill())
    registry.register(OperationModeSkill())
    return registry
