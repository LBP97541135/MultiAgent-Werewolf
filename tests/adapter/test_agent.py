"""Tests for adapter/agent.py."""

import pytest

from llm_werewolf.adapter.agent import AgentScopeWerewolfAgent


def test_agentscope_agent_init_and_helpers() -> None:
    agent = AgentScopeWerewolfAgent(name="P1", number=5, role="prophet", plan="稳健")
    assert agent.name == "P1"
    assert agent.number == 5
    assert len(agent.chat_history) == 1
    assert agent.chat_history[0]["role"] == "system"

    assert agent.extract_target("我选择 [[7]]") == 7
    assert agent.extract_content("发言 [[hello world]]") == "hello world"
    assert agent.is_wolf is False


@pytest.mark.asyncio
async def test_direct_model_fallback_response() -> None:
    agent = AgentScopeWerewolfAgent(name="P1", number=2)
    response = await agent.get_response("守卫请睁眼")
    assert response == "[[2]]"


def test_generate_fallback_yes_no() -> None:
    agent = AgentScopeWerewolfAgent(name="P1", number=1)
    response = agent._generate_fallback_response("Reply YES or NO", "err")
    assert response in ("[[0]]", "[[1]]")


def test_lazy_import_agentscope_agent_class() -> None:
    pytest.importorskip("agentscope")
    from llm_werewolf.adapter import AgentScopeWerewolfAgent as LazyAgent

    assert LazyAgent is AgentScopeWerewolfAgent
