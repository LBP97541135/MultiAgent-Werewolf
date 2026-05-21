"""Adapter layer for AgentScope integration and unified prompts."""

from typing import TYPE_CHECKING

from llm_werewolf.adapter.message import MessageAdapter, Msg
from llm_werewolf.adapter.prompt_manager import PromptManager
from llm_werewolf.adapter.prompts import GamePrompts, PlanStrategies, SYSTEM_PROMPT

if TYPE_CHECKING:
    from llm_werewolf.adapter.agent import AgentScopeWerewolfAgent

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
        from llm_werewolf.adapter.agent import AgentScopeWerewolfAgent

        return AgentScopeWerewolfAgent
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
