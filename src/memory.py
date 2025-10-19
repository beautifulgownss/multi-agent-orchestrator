"""Simple JSON-based memory store for agent interactions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from .utils.logger import console


@dataclass
class MemoryStore:
    """Persist agent outputs between runs."""

    path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent / "data" / "memory.json"
    )
    _buffer: List[Dict[str, Any]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self._buffer = self._read()

    def record(self, agent: str, content: Dict[str, Any]) -> None:
        """Append a new agent entry and persist immediately."""
        entry = {"agent": agent, **content}
        self._buffer.append(entry)
        self._write()
        console.log(f"[dim]Memory updated with {agent} output[/dim]")

    def get_all(self) -> List[Dict[str, Any]]:
        """Return all stored records."""
        return list(self._buffer)

    def clear(self) -> None:
        """Remove all stored interactions."""
        self._buffer.clear()
        if self.path.exists():
            self.path.unlink()

    def _read(self) -> List[Dict[str, Any]]:
        import json

        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write(self) -> None:
        import json

        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(self._buffer, handle, indent=2)


__all__ = ["MemoryStore"]
