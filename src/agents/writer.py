"""Writer agent that assembles the final narrative response."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class WriterAgent:
    """Blend plan structure and research context into a polished output."""

    tone: str = "professional"

    def compose(self, goal: str, plan: Iterable[str], research_notes: List[Dict[str, str]]) -> str:
        """Build a cohesive answer based on planner and researcher output."""
        intro = [
            f"Goal: {goal.strip()}",
            f"Tone: {self.tone}",
            "",
            "Approach:",
        ]

        plan_lines = [f"  {index}. {task}" for index, task in enumerate(plan, start=1)]

        research_lines = ["\nEvidence & Considerations:"]
        for note in research_notes:
            research_lines.append(f"- {note['summary']}")

        conclusion = [
            "\nRecommended Next Steps:",
            "- Validate the synthesized insights with stakeholders.",
            "- Iterate on the response as new information appears.",
        ]

        sections = intro + plan_lines + research_lines + conclusion
        return "\n".join(sections)


__all__ = ["WriterAgent"]
