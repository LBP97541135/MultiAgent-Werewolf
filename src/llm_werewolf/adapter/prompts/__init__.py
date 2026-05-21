"""Unified Chinese prompt templates for AgentScope-managed agents."""

from llm_werewolf.adapter.prompts.game import GamePrompts, PlanStrategies
from llm_werewolf.adapter.prompts.identity import IDENTITY_PROMPTS, format_identity_prompt
from llm_werewolf.adapter.prompts.system import SYSTEM_PROMPT

__all__ = [
    "GamePrompts",
    "IDENTITY_PROMPTS",
    "PlanStrategies",
    "SYSTEM_PROMPT",
    "format_identity_prompt",
]
