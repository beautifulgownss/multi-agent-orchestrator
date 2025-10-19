"""CLI entry point for running the multi-agent orchestration demo."""

from __future__ import annotations

import argparse

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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    orchestrator = Orchestrator()

    if args.clear_memory:
        log_step("Clearing stored memory")
        orchestrator.memory.clear()

    goal = args.goal or input("Enter your goal for the agents: ")
    orchestrator.run(goal)


if __name__ == "__main__":
    main()
