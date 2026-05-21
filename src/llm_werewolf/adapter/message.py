"""Backward-compatible re-export; prefer ``llm_werewolf.integration.message``."""

from llm_werewolf.integration.message import MessageAdapter, Msg

__all__ = ["MessageAdapter", "Msg"]
