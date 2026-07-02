from __future__ import annotations

import httpx
import pytest
import respx

from crucible.landscape import search_arxiv, search_literature, search_semantic_scholar

ARXIV_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2301.00001v1</id>
    <title>A Test Paper About Reward-Free RL</title>
    <author><name>Alice Smith</name></author>
    <summary>We study reward-free exploration in reinforcement learning.</summary>
    <published>2023-01-01T00:00:00Z</published>
  </entry>
</feed>"""

SS_RESPONSE = {
    "data": [
        {
            "title": "A Semantic Scholar Paper",
            "authors": [{"name": "Bob Jones"}],
            "abstract": "Abstract text here.",
            "url": "https://www.semanticscholar.org/paper/abc123",
            "externalIds": {"ArXiv": "2302.00001"},
            "year": 2023,
            "venue": "NeurIPS",
        }
    ]
}


@pytest.mark.asyncio
async def test_search_arxiv():
    with respx.mock:
        respx.get("http://export.arxiv.org/api/query").mock(
            return_value=httpx.Response(200, text=ARXIV_RESPONSE)
        )
        papers = await search_arxiv("reward-free RL", limit=5)
    assert len(papers) == 1
    assert "Reward-Free" in papers[0].title
    assert papers[0].arxiv_id == "2301.00001"


@pytest.mark.asyncio
async def test_search_semantic_scholar():
    with respx.mock:
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
            return_value=httpx.Response(200, json=SS_RESPONSE)
        )
        papers = await search_semantic_scholar("reward-free RL", limit=5)
    assert len(papers) == 1
    assert papers[0].title == "A Semantic Scholar Paper"
    assert papers[0].venue == "NeurIPS"


@pytest.mark.asyncio
async def test_search_literature_deduplicates():
    with respx.mock:
        respx.get("http://export.arxiv.org/api/query").mock(
            return_value=httpx.Response(200, text=ARXIV_RESPONSE)
        )
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
            return_value=httpx.Response(200, json=SS_RESPONSE)
        )
        papers = await search_literature("reward-free RL", limit=5)
    assert len(papers) == 2  # different arxiv ids — no dedup
