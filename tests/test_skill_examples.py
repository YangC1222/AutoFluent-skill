"""Validate examples against real MCP schemas."""

import json
from pathlib import Path

import pytest

from autofluent_mcp.advanced import AxialInput, PreflightInput, SweepInput
from autofluent_mcp.engineering import GridInput, PressureInput, TheoryInput


@pytest.mark.parametrize(
    "name,model",
    [
        ("preflight", PreflightInput),
        ("axial-heat", AxialInput),
        ("pressure", PressureInput),
        ("grid-study", GridInput),
        ("correlations", TheoryInput),
        ("sweep", SweepInput),
    ],
)
def test_skill_example_matches_mcp_schema(name, model):
    root = Path(__file__).resolve().parents[1]
    path = root / "skills" / ("autofluent-" + name) / "references/example.json"
    model.model_validate(json.loads(path.read_text(encoding="utf-8"))["spec"])
