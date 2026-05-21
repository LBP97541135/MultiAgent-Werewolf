"""Tests for adapter/prompts.py."""

from llm_werewolf.adapter.prompts import GamePrompts, PlanStrategies, RolePrompts


def test_role_prompts_base_format() -> None:
    prompt = RolePrompts.BASE_PROMPT.format(
        number=3,
        role_name="预言家",
        role_instruction="查验身份",
        suggestion="积极发言",
        plan=PlanStrategies.DEFAULT["villager"],
    )
    assert "3" in prompt
    assert "预言家" in prompt
    assert "查验身份" in prompt


def test_role_prompts_villager_config() -> None:
    assert RolePrompts.VILLAGER["role_name"] == "村民"
    assert "狼人" in RolePrompts.WOLF["role_instruction"]


def test_game_prompts_constants() -> None:
    assert GamePrompts.NIGHT_BEGIN == "天黑请闭眼"
    assert "{target}" in GamePrompts.WOLF_RESULT
