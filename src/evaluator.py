"""Heuristic agent evaluator for writer outputs."""

from __future__ import annotations

import re
from typing import Dict

from .utils.logger import console


def evaluate_output(text: str) -> Dict[str, object]:
    """Score the writer output using simple heuristics (1–5 scale)."""
    stripped = text.strip()
    length_score = min(5, max(1, len(stripped) // 120 + 1))

    bullet_points = len(re.findall(r"^\s*[-*]", stripped, flags=re.MULTILINE))
    numbered_items = len(re.findall(r"^\s*\d+\.", stripped, flags=re.MULTILINE))
    structure_score = min(5, 1 + bullet_points + numbered_items)

    unique_keywords = len(set(word.lower() for word in re.findall(r"\b\w+\b", stripped)))
    variety_score = min(5, max(1, unique_keywords // 25))

    raw_score = (length_score + structure_score + variety_score) / 3
    score = round(raw_score)
    score = max(1, min(5, score))

    if score >= 4:
        comment = "Clear and coherent output."
    elif score == 3:
        comment = "Reasonable structure; could include more detail."
    else:
        comment = "Needs richer content and clearer organization."

    result = {"score": score, "comment": comment}
    console.log(f"[dim]Evaluator assigned score {score}[/dim]")
    return result


__all__ = ["evaluate_output"]
