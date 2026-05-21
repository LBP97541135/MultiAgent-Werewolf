"""Backward-compatible adapter package; use ``integration`` and ``core.prompts``."""

from llm_werewolf.core.prompts import GamePrompts, PlanStrategies, PromptManager, SYSTEM_PROMPT
from llm_werewolf.integration import MessageAdapter, Msg

__all__ = [
    "AgentScopeWerewolfAgent",
    "GamePrompts",
    "MessageAdapter",
    "Msg",
    "PlanStrategies",
    "PromptManager",
    "SYSTEM_PROMPT",
]


def __getattr__(name: str):
    if name == "AgentScopeWerewolfAgent":
        from llm_werewolf.integration.agentscope import AgentScopeWerewolfAgent

        return AgentScopeWerewolfAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
