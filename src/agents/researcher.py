"""Researcher agent that fabricates lightweight supporting context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class ResearcherAgent:
    """Generate mock research notes for each subtask."""

    detail_level: str = "medium"

    def gather_research(self, subtasks: Iterable[str]) -> List[Dict[str, str]]:
        """Return a set of short summaries for each subtask."""
        research_notes: List[Dict[str, str]] = []

        for index, subtask in enumerate(subtasks, start=1):
            summary = self._summarize(subtask, index)
            research_notes.append({"subtask": subtask, "summary": summary})

        return research_notes

    def _summarize(self, subtask: str, index: int) -> str:
        detail_prefix = {
            "low": "High-level insight",
            "medium": "Key findings",
            "high": "Comprehensive breakdown",
        }.get(self.detail_level, "Key findings")

        return (
            f"{detail_prefix} #{index}: "
            f"- outline the core need in '{subtask}'. "
            f"- list supporting evidence or examples. "
            f"- highlight potential risks, trade-offs, and opportunities."
        )


__all__ = ["ResearcherAgent"]
