# Multi-Agent Orchestrator

A minimal Python 3.11+ project that demonstrates how three lightweight AI-style agents (Planner → Researcher → Writer) can collaborate to satisfy a user request. The system is intentionally simple and avoids external API calls so it can run anywhere.

## Features
- Planner agent turns a goal into 2–3 concrete subtasks.
- Researcher agent generates mock supporting context per subtask.
- Writer agent blends structure and notes into a final response.
- Orchestrator coordinates agents, persists outputs, and logs progress with Rich.
- Memory stored in `data/memory.json` so previous runs can be inspected or cleared.

## Project Layout
```
multi-agent-orchestrator/
├── src/
│   ├── main.py
│   ├── orchestrator.py
│   ├── memory.py
│   ├── agents/
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   └── writer.py
│   └── utils/
│       └── logger.py
├── demo/
│   └── example_output.txt
├── requirements.txt
└── README.md
```

## Getting Started
1. **Install dependencies** (Python 3.11+):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the orchestration demo**:
   ```bash
   python -m src.main --goal "Outline a strategy for launching a developer advocacy program."
   ```
   Omit `--goal` to be prompted interactively. Add `--clear-memory` to wipe prior run history.

3. **Explore stored memory**:
   Inspect `data/memory.json` to review agent outputs across runs.

## Skills Demonstrated
- Simple multi-agent coordination pattern.
- Rich console logging with color-coded stages.
- Lightweight persistent memory using JSON.
- Clean project structure ready for extension (e.g., swap in real LLM calls or expose via FastAPI).
