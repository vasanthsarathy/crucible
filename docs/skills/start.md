# `crucible:start`

> Start a new Review-Driven Development project from a seed idea.

## When to use

At the very beginning — you have an idea (a sentence, a question, an observation)
and want to turn it into a tracked RDD project.

## What it does

1. **Gather the seed** — asks for your idea without pushing you to formalize it yet.
2. **Worthiness check** — a fast two-reviewer gut-check (Flash + Copernicus):
   "is this worth pursuing?" — before you invest.
3. **Create project state** — initializes `.crucible/<project-id>/` (or the MCP
   project), records the seed and target venue.
4. **Orient** — explains the first real stage (PROBLEM) and what a passing gate
   looks like.

## Modes

- **MCP:** uses `crucible_create_project` and related tools.
- **File:** writes `state.json` and the initial `sections/` directly.

## Related

- Next: develop the PROBLEM stage, then [`crucible:reviewer-round`](reviewer-round.md).
- Advance with [`crucible:advance`](advance.md).
