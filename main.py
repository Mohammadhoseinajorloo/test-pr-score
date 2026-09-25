"""
Core utility for string sanitization and function complexity validation.
Following Clean Code principles: Pure functions, strict type hints, zero side effects.
"""

import re
from typing import Optional


def sanitize_branch_name(name: str) -> str:
    """
    Sanitizes git branch names to prevent injection and invalid refs.
    Replaces spaces and invalid characters with hyphens.
    """
    if not name or not isinstance(name, str):
        raise ValueError("Branch name must be a non-empty string.")

    cleaned = re.sub(r"[^a-zA-Z0-9/_-]", "-", name.strip().lower())
    cleaned = re.sub(r"-+", "-", cleaned)  # Deduplicate consecutive hyphens
    return cleaned.strip("-")


def calculate_complexity_score(lines_of_code: int, cyclomatic_complexity: int) -> int:
    """
    Computes a simple clean-code maintainability index for a single function.
    Returns a score between 0 and 100.
    """
    if lines_of_code < 0 or cyclomatic_complexity < 1:
        raise ValueError("Invalid metrics provided.")

    # Penalize long functions (> 30 lines) and high branch complexity (> 5)
    loc_penalty = max(0, (lines_of_code - 25) * 2)
    cc_penalty = max(0, (cyclomatic_complexity - 4) * 8)

    score = 100 - (loc_penalty + cc_penalty)
    return max(0, min(100, score))


def is_ready_for_production(score: int, min_threshold: int = 80) -> bool:
    """Determines whether a code block passes the health threshold."""
    return score >= min_threshold
