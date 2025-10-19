"""Utility helpers for colorful console logging with Rich."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme


_theme = Theme(
    {
        "step": "bold cyan",
        "agent": "magenta",
        "result": "bold green",
        "error": "bold red",
    }
)

console = Console(theme=_theme)


def log_step(message: str) -> None:
    """Highlight a high-level orchestration step."""
    console.print(f"[step]➜ {message}")


def log_agent(agent_name: str, message: str) -> None:
    """Log agent-specific updates within a framed panel."""
    console.print(
        Panel.fit(
            message,
            title=f"[agent]{agent_name}[/agent]",
            border_style="agent",
        )
    )


def log_result(result: str) -> None:
    """Print the final generated output."""
    console.print(Panel(result, title="[result]Final Output[/result]", border_style="result"))


__all__ = ["console", "log_step", "log_agent", "log_result"]
