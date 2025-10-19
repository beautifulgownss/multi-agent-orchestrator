"""Main orchestration flow for coordinating planner, researcher, and writer agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .agents.planner import PlannerAgent
from .agents.researcher import ResearcherAgent
from .agents.writer import WriterAgent
from .evaluator import evaluate_output
from .memory import load_memory, overwrite_memory, save_memory
from .utils.logger import log_agent, log_result, log_step


@dataclass
class Orchestrator:
    """Coordinate agents in sequence and persist their outputs."""

    planner: PlannerAgent = field(default_factory=PlannerAgent)
    researcher: ResearcherAgent = field(default_factory=ResearcherAgent)
    writer: WriterAgent = field(default_factory=WriterAgent)

    def run(self, goal: str) -> str:
        """Execute the end-to-end orchestration pipeline."""
        memory_payload = load_memory()
        runs = memory_payload.get("runs", [])
        recent_runs = runs[-3:]
        context_summary = "\n\n".join(
            run.get("final_output", "") for run in recent_runs if run.get("final_output")
        ).strip()
        planner_input = goal.strip()
        if context_summary:
            planner_input = f"{planner_input}\n\nPrevious context:\n{context_summary}"

        log_step("Planner is mapping the goal to subtasks")
        plan: List[str] = self.planner.create_plan(planner_input)
        log_agent("Planner", "\n".join(plan))

        log_step("Researcher is collecting supporting context")
        research_notes = self.researcher.gather_research(plan)
        formatted_notes = "\n\n".join(
            f"Subtask: {note['subtask']}\nSummary: {note['summary']}" for note in research_notes
        )
        log_agent("Researcher", formatted_notes)

        log_step("Writer is synthesizing the final answer")
        final_answer = self.writer.compose(goal, plan, research_notes)
        log_agent("Writer", final_answer)

        evaluation = evaluate_output(final_answer)
        score_color = "green" if evaluation["score"] >= 4 else "yellow" if evaluation["score"] == 3 else "red"
        log_agent(
            "Evaluator",
            f"[{score_color}]Score: {evaluation['score']}[/]\nComment: {evaluation['comment']}",
        )

        save_memory(
            {
                "goal": goal,
                "planner_output": plan,
                "researcher_output": research_notes,
                "final_output": final_answer,
                "evaluation": evaluation,
            }
        )

        log_result(final_answer)
        return final_answer

    def reevaluate_runs(self) -> None:
        """Re-score existing runs without executing the agents."""
        payload = load_memory()
        runs = payload.get("runs", [])
        if not runs:
            log_step("No stored runs found to evaluate.")
            return

        log_step(f"Re-evaluating {len(runs)} stored runs")
        for index, run in enumerate(runs, start=1):
            final_output = run.get("final_output", "")
            if not final_output:
                log_agent("Evaluator", f"[red]Run {index} missing final_output; skipping[/red]")
                continue

            evaluation = evaluate_output(final_output)
            run["evaluation"] = evaluation
            score_color = (
                "green" if evaluation["score"] >= 4 else "yellow" if evaluation["score"] == 3 else "red"
            )
            log_agent(
                "Evaluator",
                f"Run {index} [{score_color}]Score: {evaluation['score']}[/]\nComment: {evaluation['comment']}",
            )

        overwrite_memory(payload)


__all__ = ["Orchestrator"]
