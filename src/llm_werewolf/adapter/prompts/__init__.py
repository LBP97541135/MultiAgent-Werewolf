"""Backward-compatible re-export; prefer ``llm_werewolf.core.prompts``."""

from llm_werewolf.core.prompts import (
    GamePrompts,
    IDENTITY_PROMPTS,
    PlanStrategies,
    SYSTEM_PROMPT,
    format_identity_prompt,
)

__all__ = [
    "GamePrompts",
    "IDENTITY_PROMPTS",
    "PlanStrategies",
    "SYSTEM_PROMPT",
    "format_identity_prompt",
]
