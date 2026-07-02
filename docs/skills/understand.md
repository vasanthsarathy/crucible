# `crucible:understand`

> Ad-hoc Socratic understanding check on any concept in your project.

## When to use

Mid-session, when you realize you're not sure you actually understand something —
a method, a definition, a claim you're leaning on. Use it before it bites you at a
gate.

## What it does

1. Asks you to name the concept.
2. Runs a short Socratic probe — open questions that surface whether you can
   explain it in your own words.
3. **Logs the outcome** — gaps and clarifications go to the understanding log and
   feed the concept map (`encountered → explained → applied`).

## Modes

- **MCP:** `crucible_log_understanding_check`, updating `crucible_update_concept_status`.
- **File:** appends to `understanding_log/` and updates `concepts.json`.

## Related

- The gate-time version of this is built into [`crucible:advance`](advance.md).
- See tracked concepts in [`crucible:status`](status.md).
