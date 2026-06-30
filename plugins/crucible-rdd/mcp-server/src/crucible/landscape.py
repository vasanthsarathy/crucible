from __future__ import annotations
import xml.etree.ElementTree as ET
from typing import Optional
import httpx
from .models import Paper

ARXIV_API = "http://export.arxiv.org/api/query"
SS_API = "https://api.semanticscholar.org/graph/v1/paper/search"
ATOM_NS = "http://www.w3.org/2005/Atom"


async def search_arxiv(query: str, limit: int = 10) -> list[Paper]:
    params = {"search_query": f"all:{query}", "max_results": limit, "sortBy": "relevance"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(ARXIV_API, params=params)
        resp.raise_for_status()
    root = ET.fromstring(resp.text)
    papers = []
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        raw_id = (entry.findtext(f"{{{ATOM_NS}}}id") or "").strip()
        arxiv_id = raw_id.split("/abs/")[-1].split("v")[0] if "/abs/" in raw_id else None
        title = (entry.findtext(f"{{{ATOM_NS}}}title") or "").strip()
        abstract = (entry.findtext(f"{{{ATOM_NS}}}summary") or "").strip()
        authors = [a.findtext(f"{{{ATOM_NS}}}name") or "" for a in entry.findall(f"{{{ATOM_NS}}}author")]
        published = entry.findtext(f"{{{ATOM_NS}}}published") or ""
        year = int(published[:4]) if published else None
        url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else raw_id
        papers.append(Paper(title=title, authors=authors, abstract=abstract, url=url, arxiv_id=arxiv_id, year=year))
    return papers


async def search_semantic_scholar(query: str, limit: int = 10) -> list[Paper]:
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,abstract,url,externalIds,year,venue",
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(SS_API, params=params)
        resp.raise_for_status()
    data = resp.json().get("data", [])
    papers = []
    for item in data:
        papers.append(Paper(
            title=item.get("title", ""),
            authors=[a.get("name", "") for a in item.get("authors", [])],
            abstract=item.get("abstract", "") or "",
            url=item.get("url", ""),
            arxiv_id=(item.get("externalIds") or {}).get("ArXiv"),
            year=item.get("year"),
            venue=item.get("venue"),
        ))
    return papers


async def search_literature(query: str, limit: int = 10) -> list[Paper]:
    """Search both arXiv and Semantic Scholar, deduplicate by arxiv_id."""
    arxiv_papers: list[Paper] = []
    ss_papers: list[Paper] = []
    try:
        arxiv_papers = await search_arxiv(query, limit)
    except Exception:
        pass
    try:
        ss_papers = await search_semantic_scholar(query, limit)
    except Exception:
        pass
    seen_keys: set[str] = set()
    results = []
    for p in arxiv_papers + ss_papers:
        key = p.arxiv_id or p.url
        if key not in seen_keys:
            seen_keys.add(key)
            results.append(p)
    return results[:limit]
