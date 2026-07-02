# `crucible:status`

> A dashboard for the active research project.

## When to use

Any time you want to see where you stand — start of a session, before deciding
what to work on, or before attempting a gate.

## What it shows

- **Current stage** and target venue.
- **Section completion** across `sections/`.
- **Last reviewer round** verdicts and open concerns.
- **Concept gaps** from the concept map (what's encountered but not yet explained
  or applied).
- **Recent ideas** captured in the ideas log.

## Modes

- **MCP:** reads via `crucible_list_projects` and related query tools.
- **File:** reads `state.json`, `sections/`, `review_rounds/`, `concepts.json`,
  `ideas_log.json` directly.

## Related

- Address gaps with [`crucible:understand`](understand.md).
- Get fresh feedback with [`crucible:reviewer-round`](reviewer-round.md).
