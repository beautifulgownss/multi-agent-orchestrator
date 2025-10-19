# Multi-Agent Orchestrator

## 🧠 Overview
A multi-agent orchestration system where Planner, Researcher, and Writer collaborate to complete complex goals using shared memory, structured prompts, and observable state.

## 🚀 Features
- Sequenced Planner → Researcher → Writer pipeline
- Rich logging for observability
- JSON-based persistent memory with recall across sessions
- CLI interface with `--clear-memory` flag
- Modular architecture ready for UI or API integration
- Optional evaluation and guardrails layer for reliability

## ⚙️ Installation & Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --goal "Plan a product launch strategy"
python -m src.main --clear-memory # optional reset
```

## 🧩 Architecture
```
User Input → Planner → Researcher → Writer → Evaluator → Memory (JSON)
```

## 🪶 Persistent Memory
- `data/memory.json` captures each run with goal, agent outputs, evaluation, and timestamps.
- The orchestrator threads in the final outputs from the three most recent runs as prior context for the Planner.
- This showcases long-lived agent state and continuity across sessions for richer, more coherent responses.

## 🔍 Evaluation Layer
- A heuristic evaluator scores Writer outputs (1–5) using length, structure, and keyword variety.
- Results are logged in memory and surfaced in the CLI with Rich for immediate feedback.
- `python -m src.main --evaluate-only` recalculates scores for stored runs without re-running agents.

## 🧰 Tech Stack
- Python 3.11+
- Rich for structured console output
- LangGraph / CrewAI-ready agent interfaces
- OpenAI SDK placeholder for future LLM integration
- FastAPI-ready for API exposure (optional)

## 🎥 Demo
- Review `demo/example_output.txt` for a sample run, including evaluation metadata.
- Run the CLI interactively to generate new outputs and inspect `data/memory.json` for stored history.

## 🧠 Skills Demonstrated
- Agent orchestration and reasoning
- Prompt architecture and message passing
- State management and persistence
- Evaluation and introspection
- Applied AI systems engineering
