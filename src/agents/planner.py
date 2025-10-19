"""Planner agent that maps a high-level goal to actionable subtasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PlannerAgent:
    """Break down user goals into manageable subtasks."""

    max_steps: int = 3

    def create_plan(self, goal: str) -> List[str]:
        """Generate a short ordered list of subtasks."""
        normalized = goal.strip().rstrip(".")

        plan = [
            f"Frame the objective and success criteria for: {normalized}",
            f"Identify key insights, data points, or examples relevant to: {normalized}",
            f"Synthesize findings into a structured response addressing: {normalized}",
        ]

        return plan[: self.max_steps]


__all__ = ["PlannerAgent"]
