from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class WorkflowState:
    session_id: str
    workflow_id: str
    status: str = "pending"
    current_step: str | None = None
    steps_history: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def touch(self) -> None:
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mark_running(self) -> None:
        self.status = "running"
        self.touch()

    def mark_waiting_for_confirmation(self, step: str) -> None:
        self.status = "waiting_for_confirmation"
        self.current_step = step
        self.touch()

    def mark_completed(self) -> None:
        self.status = "completed"
        self.touch()

    def mark_rejected(self) -> None:
        self.status = "rejected"
        self.touch()

    def add_history(self, step: str, result: dict[str, Any]) -> None:
        self.steps_history.append({
            "step": step,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        self.touch()

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "workflow_id": self.workflow_id,
            "status": self.status,
            "current_step": self.current_step,
            "steps_history": self.steps_history,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
