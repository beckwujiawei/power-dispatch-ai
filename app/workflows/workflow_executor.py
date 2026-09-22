from __future__ import annotations

from app.agent.communication_agent import CommunicationAgent


class WorkflowExecutor:
    def __init__(self, agent: CommunicationAgent | None = None):
        self.agent = agent or CommunicationAgent()

    def run(self, message: str, *, session_id: str = "demo-session", operator: str = "演示调度员"):
        return self.agent.handle(message, session_id=session_id, operator=operator)
