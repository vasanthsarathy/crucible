import json

import pytest
from mcp.server.fastmcp import FastMCP

from crucible.server import create_server


# Helper: FastMCP.call_tool returns (content_list, raw_dict).
# We wrap it so tests can use result.content[0].text as the spec intends.
class ToolResult:
    def __init__(self, content):
        self.content = content

    @classmethod
    async def call(cls, server: FastMCP, name: str, args: dict) -> "ToolResult":
        content, _raw = await server.call_tool(name, args)
        return cls(content)


@pytest.fixture
def base_dir(tmp_path):
    return tmp_path / ".crucible"


@pytest.fixture
def server(base_dir):
    return create_server(base_dir=base_dir)


@pytest.mark.asyncio
async def test_create_and_get_project(server):
    result = await ToolResult.call(
        server,
        "crucible_create_project",
        {
            "name": "Test Paper",
            "seed_idea": "What if we challenged IID?",
            "target_venue": "NeurIPS",
        },
    )
    project_id = result.content[0].text
    assert project_id is not None

    result2 = await ToolResult.call(server, "crucible_get_project", {"project_id": project_id})
    state = json.loads(result2.content[0].text)
    assert state["name"] == "Test Paper"
    assert state["current_stage"] == "SEED"


@pytest.mark.asyncio
async def test_update_and_get_section(server):
    result = await ToolResult.call(
        server, "crucible_create_project", {"name": "Test", "seed_idea": "seed"}
    )
    pid = result.content[0].text
    await ToolResult.call(
        server,
        "crucible_update_section",
        {"project_id": pid, "section": "problem", "content": "## Problem\n\nLet $X$ be a set."},
    )
    result2 = await ToolResult.call(
        server, "crucible_get_section", {"project_id": pid, "section": "problem"}
    )
    assert "Let $X$" in result2.content[0].text


@pytest.mark.asyncio
async def test_advance_stage(server):
    result = await ToolResult.call(
        server, "crucible_create_project", {"name": "Test", "seed_idea": "seed"}
    )
    pid = result.content[0].text
    result2 = await ToolResult.call(server, "crucible_advance_stage", {"project_id": pid})
    assert "PROBLEM" in result2.content[0].text


@pytest.mark.asyncio
async def test_list_projects(server):
    await ToolResult.call(server, "crucible_create_project", {"name": "A", "seed_idea": "seed a"})
    await ToolResult.call(server, "crucible_create_project", {"name": "B", "seed_idea": "seed b"})
    result = await ToolResult.call(server, "crucible_list_projects", {})
    projects = json.loads(result.content[0].text)
    assert len(projects) == 2


@pytest.mark.asyncio
async def test_get_reviewer_personas(server):
    result = await ToolResult.call(
        server, "crucible_create_project", {"name": "Test", "seed_idea": "seed"}
    )
    pid = result.content[0].text
    result2 = await ToolResult.call(server, "crucible_get_reviewer_personas", {"project_id": pid})
    personas = json.loads(result2.content[0].text)
    assert len(personas) == 7
