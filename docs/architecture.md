# Architecture

## Skills-primary design

Crucible is **skills-primary**: the five `crucible:*` skills are the product. Each
skill is a Markdown procedure Claude follows. They work with **no server** by
reading and writing plain files under `.crucible/`. When the optional MCP server
is running, the skills detect it and delegate state operations to it instead —
gaining structured queries, cross-session concept tracking, and live literature
search. This is the "Step 0: Check for MCP" block at the top of every skill.

```text
                 ┌─────────────────────────────┐
   /crucible:*   │  skill (Markdown procedure)  │
   ───────────►  │  Step 0: MCP available?      │
                 └──────────────┬──────────────┘
                    yes │        │ no
                        ▼        ▼
              ┌───────────────┐ ┌───────────────────┐
              │  MCP server   │ │  direct .crucible/ │
              │  (crucible_*) │ │  file read/write   │
              └───────┬───────┘ └─────────┬─────────┘
                      └────────┬──────────┘
                               ▼
                        .crucible/<project-id>/
```

## The gate model

Work moves through stages `SEED → PROBLEM → SURVEY → SOLUTION → DEVELOP → PAPER`.
Advancing is gated twice, both enforced by [`crucible:advance`](skills/advance.md):

1. **Reviewer gate** — the seven-persona panel evaluates the stage. At least 3 of
   the 5 voting reviewers must give accept/revise with no outright reject.
   Linnaeus and Socrates always contribute required revisions.
2. **Socratic probe** — you answer 2–3 open questions from memory. Gaps are logged;
   the stage doesn't advance until understanding is demonstrated.

Every gate is preceded by a **Devil's Advocate pass**. Reviewer weighting shifts by
target venue (see the venue profiles in the plugin README).

## State layout

All state lives under `.crucible/<project-id>/` as plain Markdown + JSON —
version-controllable, no server required:

| Path | Contents |
| --- | --- |
| `state.json` | current stage, venue, timestamps |
| `sections/` | `abstract.md`, `problem.md`, `survey.md`, … |
| `experiments/` | runnable scripts + results |
| `review_rounds/` | every reviewer round as JSON |
| `understanding_log/` | Socratic probe history |
| `assumptions_log.json` | surfaced assumptions (feed the Limitations section) |
| `ideas_log.json` | captured tangents / future directions |
| `stage_history.json` | stage transitions |
| `concepts.json` | concept map (encountered → explained → applied) |

## MCP server

A small Python (FastMCP) server under `plugins/crucible-rdd/mcp-server/`. It exposes
`crucible_*` tools backed by the same `.crucible/` store, plus `landscape` search
against arXiv and Semantic Scholar. Launched via `uv run` (cross-platform) as wired
in `plugin.json`. Source is organized as `server.py` (tools), `store.py`
(persistence), `models.py` (typed schemas), `reviewer_personas.py`,
`venue_profiles.py`, and `landscape.py`.
