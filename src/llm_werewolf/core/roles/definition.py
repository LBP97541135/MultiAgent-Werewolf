"""Role definition schema (name, skill, camp, victory goal)."""

from pydantic import Field, BaseModel

from llm_werewolf.core.types.enums import Camp, VictoryGoal


class RoleDefinition(BaseModel):
    """Declarative role metadata used for registration and prompts.

    Fields:
        name: Registry key (e.g. ``Seer``), matches skill class registry name.
        display_name: Human-readable Chinese name shown to players.
        skill: Import path ``module:Class`` for the role implementation.
        camp: Faction / identity camp.
        victory_goal: Win-condition category for documentation and prompts.
    """

    name: str = Field(..., description="Registry key, e.g. Seer")
    display_name: str = Field(..., description="Chinese display name")
    skill: str = Field(
        ...,
        description="Skill implementation as module:Class, e.g. llm_werewolf.core.roles.villager:Seer",
    )
    camp: Camp = Field(..., description="Faction camp")
    victory_goal: VictoryGoal = Field(..., description="Victory objective category")
