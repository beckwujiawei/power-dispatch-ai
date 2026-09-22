from __future__ import annotations

from typing import Any

from app.workflows.workflow_state import WorkflowState


class WorkflowManager:
    def __init__(self):
        self._workflows: dict[str, WorkflowState] = {}

    def create(self, session_id: str, workflow_id: str | None = None) -> WorkflowState:
        flow_id = workflow_id or f"WF-{session_id}-{len(self._workflows) + 1}"
        state = WorkflowState(session_id=session_id, workflow_id=flow_id)
        self._workflows[flow_id] = state
        return state

    def get(self, workflow_id: str) -> WorkflowState | None:
        return self._workflows.get(workflow_id)

    def get_by_session(self, session_id: str) -> WorkflowState | None:
        for state in self._workflows.values():
            if state.session_id == session_id:
                return state
        return None

    def list(self) -> list[WorkflowState]:
        return list(self._workflows.values())

    def update(self, workflow_id: str, **kwargs: Any) -> WorkflowState | None:
        state = self._workflows.get(workflow_id)
        if state is None:
            return None
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        state.touch()
        return state
