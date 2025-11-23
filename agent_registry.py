"""Agent registry loader using PyYAML.

This module provides the :class:`AgentRegistry` which loads agent metadata from
YAML files and exposes a simple API for retrieving formatted prompts for each
agent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional

import yaml


def _as_list(value: Any) -> List[str]:
    """Normalise a YAML scalar or sequence into a list of strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        result: List[str] = []
        for item in value:
            if item is None:
                continue
            result.append(str(item))
        return result
    raise TypeError(f"Expected a string or sequence, received {type(value)!r}")


@dataclass
class AgentDefinition:
    """Container for a single agent definition."""

    name: str
    role: Optional[str] = None
    goal: Optional[str] = None
    description: Optional[str] = None
    backstory: Optional[str] = None
    goals: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    prompt_template: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def _format_context(self) -> MutableMapping[str, Any]:
        """Create a mapping used when rendering string templates."""

        goals_list = self.goals or ([self.goal] if self.goal else [])
        constraints = self.constraints
        tools = self.tools
        context: Dict[str, Any] = {
            "name": self.name,
            "role": self.role or "",
            "goal": self.goal or "",
            "goals": goals_list,
            "goals_bulleted": "\n".join(f"- {item}" for item in goals_list) if goals_list else "",
            "constraints": constraints,
            "constraints_bulleted": "\n".join(f"- {item}" for item in constraints) if constraints else "",
            "tools": tools,
            "tools_bulleted": "\n".join(f"- {item}" for item in tools) if tools else "",
            "tools_csv": ", ".join(tools) if tools else "none",
            "description": self.description or "",
            "backstory": self.backstory or "",
        }
        context.update(self.extra)
        return context

    def build_prompt(self) -> str:
        """Render a prompt string for the agent."""

        context = self._format_context()
        if self.prompt_template:
            from collections import defaultdict

            safe_context: MutableMapping[str, Any] = defaultdict(str, context)
            return self.prompt_template.format_map(safe_context)

        paragraphs: List[str] = []

        role_line: str
        if self.role:
            role_line = f"You are {self.name}, a {self.role}."
        else:
            role_line = f"You are {self.name}."
        paragraphs.append(role_line)

        if self.backstory:
            paragraphs.append(self.backstory.strip())
        elif self.description:
            paragraphs.append(self.description.strip())

        goals_list = context["goals"]
        if goals_list:
            goals_section = "Goals:\n" + "\n".join(f"- {item}" for item in goals_list)
            paragraphs.append(goals_section)

        if self.constraints:
            constraints_section = "Constraints:\n" + "\n".join(f"- {item}" for item in self.constraints)
            paragraphs.append(constraints_section)

        if self.tools:
            tools_section = "Tools:\n" + "\n".join(f"- {item}" for item in self.tools)
            paragraphs.append(tools_section)

        return "\n\n".join(paragraphs)


class AgentRegistry:
    """Load agent metadata from a YAML file and expose formatted prompts."""

    def __init__(self, yaml_path: Path | str):
        self._path = Path(yaml_path)
        if not self._path.exists():
            raise FileNotFoundError(f"Agent registry file not found: {self._path}")

        with self._path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}

        if not isinstance(data, Mapping):
            raise ValueError("Agent registry file must contain a YAML mapping at the top level.")

        raw_agents = data.get("agents", {})
        if not isinstance(raw_agents, Mapping):
            raise ValueError("The 'agents' key must contain a mapping of agent definitions.")

        self._agents: Dict[str, AgentDefinition] = {}
        for name, definition in raw_agents.items():
            if not isinstance(definition, Mapping):
                raise ValueError(f"Agent '{name}' must be defined using a mapping.")
            self._agents[name] = self._parse_agent(name, definition)

    @staticmethod
    def _parse_agent(name: str, definition: Mapping[str, Any]) -> AgentDefinition:
        """Convert a raw mapping into an :class:`AgentDefinition`."""

        role = definition.get("role")
        goal = definition.get("goal")
        description = definition.get("description")
        backstory = definition.get("backstory")
        goals = _as_list(definition.get("goals"))
        constraints = _as_list(definition.get("constraints"))
        tools = _as_list(definition.get("tools"))
        prompt_template = definition.get("prompt_template")

        known_keys = {
            "role",
            "goal",
            "goals",
            "description",
            "backstory",
            "constraints",
            "tools",
            "prompt_template",
        }
        extra = {key: value for key, value in definition.items() if key not in known_keys}

        return AgentDefinition(
            name=name,
            role=role,
            goal=goal,
            description=description,
            backstory=backstory,
            goals=goals,
            constraints=constraints,
            tools=tools,
            prompt_template=prompt_template,
            extra=extra,
        )

    def get_prompt(self, agent_name: str) -> str:
        """Return a fully formatted prompt for the requested agent."""

        try:
            agent = self._agents[agent_name]
        except KeyError as error:
            raise KeyError(f"Agent '{agent_name}' is not registered in {self._path}.") from error
        return agent.build_prompt()

    @property
    def agents(self) -> Mapping[str, AgentDefinition]:
        """Expose the loaded agent definitions."""

        return dict(self._agents)


__all__ = ["AgentRegistry", "AgentDefinition"]
