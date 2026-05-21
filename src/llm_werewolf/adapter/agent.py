"""AgentScope-integrated werewolf agent with unified Chinese prompts."""

import re
import asyncio
from typing import Any, Optional

from pydantic import Field

from llm_werewolf.core.agent import BaseAgent
from llm_werewolf.adapter.message import MessageAdapter, Msg
from llm_werewolf.adapter.prompt_agent import PromptAgentMixin


class AgentScopeWerewolfAgent(PromptAgentMixin, BaseAgent):
    """Werewolf player agent using AgentScope message format and unified prompts.

    System prompt + identity prompt are injected via ``bind_role`` after role assignment.
    """

    model: str = Field(default="agentscope")
    plan: str = Field(default="自由发挥")
    agentscope_agent: Any = Field(default=None, exclude=True)
    decision_history: list[str] = Field(default_factory=list)
    chat_history: list[dict[str, str]] = Field(default_factory=list)
    role_definition: object | None = Field(default=None, exclude=True)
    seat_number: int = Field(default=0, exclude=True)

    def __init__(
        self,
        name: str,
        model: str = "agentscope",
        plan: str = "自由发挥",
        agentscope_agent: Any = None,
    ) -> None:
        super().__init__(name=name, model=model)
        self.plan = plan
        self.agentscope_agent = agentscope_agent
        self.decision_history = []
        self.chat_history = []

    async def get_response(self, message: str) -> str:
        """Get response; uses AgentScope runtime when configured."""
        self.chat_history.append({"role": "user", "content": message})

        if self.agentscope_agent is not None:
            return await self._call_agentscope_agent(message)
        return await self._call_direct_model(message)

    async def _call_agentscope_agent(self, message: str) -> str:
        try:
            from agentscope.message import Msg as AgentScopeMsg
        except ImportError as exc:
            msg = (
                "需要安装 AgentScope：pip install 'llm_werewolf[agentscope]'"
            )
            raise ImportError(msg) from exc

        input_msg = AgentScopeMsg(name="Moderator", content=message, role="user")

        try:
            response_msg = await self.agentscope_agent(input_msg)
            response_text = self._extract_text(response_msg)
            if not response_text:
                response_text = self._generate_fallback_response(message)
            await asyncio.sleep(0)
        except Exception:
            response_text = self._generate_fallback_response(message)

        self.chat_history.append({"role": "assistant", "content": response_text})
        return response_text

    @staticmethod
    def _extract_text(response_msg: Any) -> str:
        if hasattr(response_msg, "get_text_content"):
            return response_msg.get_text_content() or ""
        if hasattr(response_msg, "content"):
            content = response_msg.content
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                texts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            texts.append(block.get("text", ""))
                        elif "text" in block:
                            texts.append(block["text"])
                    elif isinstance(block, str):
                        texts.append(block)
                return "\n".join(texts)
            return str(content)
        return str(response_msg)

    def _generate_fallback_response(self, message: str) -> str:
        import random

        if "[[1]]" in message and "[[0]]" in message:
            return random.choice(["[[1]]", "[[0]]"])  # noqa: S311

        if "[[]]" in message or "编号" in message or "可选目标" in message:
            numbers = re.findall(r"(\d+)\.", message)
            if numbers:
                return f"[[{random.choice(numbers)}]]"  # noqa: S311
            return f"[[{random.randint(1, 12)}]]"  # noqa: S311

        if "投票" in message:
            return f"[[{random.randint(0, 12)}]]"  # noqa: S311

        speeches = [
            "[[我觉得场上局势很复杂，需要再观察]]",
            "[[我倾向于相信发言更自然的玩家]]",
            "[[我是好人，会继续分析]]",
        ]
        return random.choice(speeches)  # noqa: S311

    async def _call_direct_model(self, message: str) -> str:
        """Fallback when no AgentScope runtime agent is attached."""
        import random

        if "[[1]]" in message and "[[0]]" in message:
            return random.choice(["[[1]]", "[[0]]"])  # noqa: S311
        if "可选目标" in message or "编号" in message:
            return f"[[{self.seat_number or 1}]]"
        return "[[我同意当前分析]]"

    def add_decision(self, decision: str) -> None:
        self.decision_history.append(decision)

    def get_decision_context(self) -> str:
        if not self.decision_history:
            return ""
        return "\n\n你此前的决策记录：\n" + "\n".join(f"- {d}" for d in self.decision_history)

    def extract_target(self, text: str) -> Optional[int]:
        match = re.search(r"\[\[\s*(\d+)\s*\]\]", text)
        if match:
            return int(match.group(1))
        return None

    def extract_content(self, text: str) -> Optional[str]:
        match = re.search(r"\[\[\s*(.+?)\s*\]\]", text, flags=re.S)
        if match:
            return match.group(1).strip()
        return None

    def reset(self) -> None:
        self.decision_history = []
        if self.role_definition is not None:
            self.chat_history = []
            self.bind_role(
                __import__(
                    self.role_definition.skill.split(":")[0],
                    fromlist=[self.role_definition.skill.split(":")[1]],
                ).__dict__[self.role_definition.skill.split(":")[1]],
                self.seat_number,
                self.plan,
            )
