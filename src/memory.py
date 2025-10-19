"""Persistent JSON-backed memory utilities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .utils.logger import console

MEMORY_PATH = Path(__file__).resolve().parent.parent / "data" / "memory.json"


def _default_payload() -> Dict[str, Any]:
    return {"runs": []}


def _ensure_memory_file() -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not MEMORY_PATH.exists():
        MEMORY_PATH.write_text(json.dumps(_default_payload(), indent=2), encoding="utf-8")


def _read_memory() -> Dict[str, Any]:
    with MEMORY_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_memory(payload: Dict[str, Any]) -> None:
    with MEMORY_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def load_memory() -> Dict[str, Any]:
    """Return the full memory payload, creating it when absent."""
    _ensure_memory_file()
    payload = _read_memory()
    runs = payload.get("runs", [])
    console.log(f"Loaded {len(runs)} prior runs into context.")
    return payload


def save_memory(run: Dict[str, Any]) -> None:
    """Append a timestamped run entry to the memory file."""
    _ensure_memory_file()
    payload = _read_memory()
    runs = payload.setdefault("runs", [])
    timestamp = datetime.now(timezone.utc).isoformat()
    runs.append({"timestamp": timestamp, **run})
    _write_memory(payload)
    console.log("Saved run to memory.json successfully.")


def overwrite_memory(payload: Dict[str, Any]) -> None:
    """Persist the provided payload, ensuring required structure exists."""
    _ensure_memory_file()
    if "runs" not in payload:
        payload["runs"] = []
    _write_memory(payload)
    console.log("Updated memory.json successfully.")


def clear_memory() -> None:
    """Delete the memory file if it exists."""
    if MEMORY_PATH.exists():
        MEMORY_PATH.unlink()
    _ensure_memory_file()


__all__ = ["MEMORY_PATH", "load_memory", "save_memory", "overwrite_memory", "clear_memory"]
