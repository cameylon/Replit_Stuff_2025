from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_registry import AgentRegistry


def test_prompt_for_researcher_includes_sections():
    registry = AgentRegistry(ROOT / "agent_registry.yaml")
    prompt = registry.get_prompt("researcher")

    assert "You are researcher, a Research Analyst." in prompt
    assert "Goals:" in prompt
    assert "Constraints:" in prompt
    assert "Tools:" in prompt


def test_prompt_for_writer_uses_template():
    registry = AgentRegistry(ROOT / "agent_registry.yaml")
    prompt = registry.get_prompt("writer")

    assert "Mission: Craft a compelling product announcement for upcoming releases." in prompt
    assert "Available tools: style_guide" in prompt


def test_unknown_agent_raises_key_error():
    registry = AgentRegistry(ROOT / "agent_registry.yaml")

    with pytest.raises(KeyError):
        registry.get_prompt("unknown")
