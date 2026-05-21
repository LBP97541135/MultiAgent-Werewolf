"""Load role skill classes from definition skill paths."""

import importlib
from typing import TypeVar

from llm_werewolf.core.roles.base import Role
from llm_werewolf.core.roles.definition import RoleDefinition

T = TypeVar("T", bound=type[Role])


def import_skill_class(skill: str) -> type[Role]:
    """Import a role class from ``module.path:ClassName``."""
    if ":" not in skill:
        msg = f"Invalid skill path '{skill}', expected format 'module:Class'"
        raise ValueError(msg)
    module_name, class_name = skill.split(":", 1)
    module = importlib.import_module(module_name)
    role_class = getattr(module, class_name)
    if not isinstance(role_class, type) or not issubclass(role_class, Role):
        msg = f"Skill '{skill}' is not a Role subclass"
        raise TypeError(msg)
    return role_class


def skill_class_from_definition(definition: RoleDefinition) -> type[Role]:
    """Resolve the Role class for a role definition."""
    return import_skill_class(definition.skill)
