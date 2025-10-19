"""Main orchestration flow for coordinating planner, researcher, and writer agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .agents.planner import PlannerAgent
from .agents.researcher import ResearcherAgent
from .agents.writer import WriterAgent
from .memory import MemoryStore
from .utils.logger import log_agent, log_result, log_step


@dataclass
class Orchestrator:
    """Coordinate agents in sequence and persist their outputs."""

    planner: PlannerAgent = field(default_factory=PlannerAgent)
    researcher: ResearcherAgent = field(default_factory=ResearcherAgent)
    writer: WriterAgent = field(default_factory=WriterAgent)
    memory: MemoryStore = field(default_factory=MemoryStore)

    def run(self, goal: str) -> str:
        """Execute the end-to-end orchestration pipeline."""
        log_step("Planner is mapping the goal to subtasks")
        plan: List[str] = self.planner.create_plan(goal)
        log_agent("Planner", "\n".join(plan))
        self.memory.record("planner", {"goal": goal, "plan": plan})

        log_step("Researcher is collecting supporting context")
        research_notes = self.researcher.gather_research(plan)
        formatted_notes = "\n\n".join(
            f"Subtask: {note['subtask']}\nSummary: {note['summary']}" for note in research_notes
        )
        log_agent("Researcher", formatted_notes)
        self.memory.record("researcher", {"notes": research_notes})

        log_step("Writer is synthesizing the final answer")
        final_answer = self.writer.compose(goal, plan, research_notes)
        log_agent("Writer", final_answer)
        self.memory.record("writer", {"final_answer": final_answer})

        log_result(final_answer)
        return final_answer


__all__ = ["Orchestrator"]
