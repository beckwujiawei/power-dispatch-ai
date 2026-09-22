from __future__ import annotations

from app.skills.base import BaseSkill


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
