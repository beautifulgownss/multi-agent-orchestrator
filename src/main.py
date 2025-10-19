"""CLI entry point for running the multi-agent orchestration demo."""

from __future__ import annotations

import argparse

from .memory import clear_memory
from .orchestrator import Orchestrator
from .utils.logger import log_step


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Planner → Researcher → Writer orchestration demo."
    )
    parser.add_argument(
        "--goal",
        type=str,
        help="High-level user goal for the agents to solve. If omitted, you will be prompted.",
    )
    parser.add_argument(
        "--clear-memory",
        action="store_true",
        help="Remove previous agent interactions before running.",
    )
    parser.add_argument(
        "--evaluate-only",
        action="store_true",
        help="Re-score stored runs without executing the agents.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    orchestrator = Orchestrator()

    if args.evaluate_only and args.clear_memory:
        raise SystemExit("--evaluate-only cannot be combined with --clear-memory.")

    if args.clear_memory:
        log_step("Clearing stored memory")
        clear_memory()

    if args.evaluate_only:
        log_step("Re-evaluating stored outputs")
        orchestrator.reevaluate_runs()
        return

    goal = args.goal or input("Enter your goal for the agents: ")
    orchestrator.run(goal)


if __name__ == "__main__":
    main()
