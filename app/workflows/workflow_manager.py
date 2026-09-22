from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.workflows.workflow_state import WorkflowState


class WorkflowManager:
    def __init__(self, store_path: str | Path | None = None):
        self.store_path = Path(store_path) if store_path is not None else Path(__file__).resolve().parent / "workflow_store.json"
        self._workflows: dict[str, WorkflowState] = {}
        self._load()

    def _persist(self) -> None:
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            workflow_id: state.to_dict()
            for workflow_id, state in self._workflows.items()
        }
        self.store_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _load(self) -> None:
        if not self.store_path.exists():
            return
        try:
            raw_data = json.loads(self.store_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        if not isinstance(raw_data, dict):
            return

        for workflow_id, value in raw_data.items():
            if not isinstance(value, dict):
                continue
            state = WorkflowState(
                session_id=value.get("session_id", "unknown-session"),
                workflow_id=workflow_id,
                status=value.get("status", "pending"),
                current_step=value.get("current_step"),
                steps_history=value.get("steps_history", []),
                created_at=value.get("created_at"),
                updated_at=value.get("updated_at"),
            )
            self._workflows[workflow_id] = state

    def create(self, session_id: str, workflow_id: str | None = None) -> WorkflowState:
        flow_id = workflow_id or f"WF-{session_id}-{len(self._workflows) + 1}"
        state = WorkflowState(session_id=session_id, workflow_id=flow_id)
        self._workflows[flow_id] = state
        self._persist()
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
        self._persist()
        return state
