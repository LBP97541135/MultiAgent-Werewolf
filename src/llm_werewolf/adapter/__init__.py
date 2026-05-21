"""Adapter layer for AgentScope integration."""

from typing import TYPE_CHECKING

from llm_werewolf.adapter.message import MessageAdapter, Msg
from llm_werewolf.adapter.prompts import GamePrompts, PlanStrategies, RolePrompts

if TYPE_CHECKING:
    from llm_werewolf.adapter.agent import AgentScopeWerewolfAgent

__all__ = [
    "AgentScopeWerewolfAgent",
    "GamePrompts",
    "MessageAdapter",
    "Msg",
    "PlanStrategies",
    "RolePrompts",
]


def __getattr__(name: str):
    if name == "AgentScopeWerewolfAgent":
        from llm_werewolf.adapter.agent import AgentScopeWerewolfAgent

        return AgentScopeWerewolfAgent
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
