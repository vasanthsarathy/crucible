# `crucible:advance`

> Check readiness to advance to the next stage: reviewer gate + Socratic probe.

## When to use

When you think the current stage is done and want to move on. This is the formal
gate — don't skip it.

## What it does

1. **Devil's Advocate pass** — argues as hard as possible against the contribution.
2. **Reviewer gate** — the full panel evaluates. Passes if ≥ 3 of the 5 voting
   reviewers give accept/revise with no outright reject. Linnaeus and Socrates
   always add required revisions that must be addressed.
3. **Socratic probe** — 2–3 open questions you answer from memory.
4. **Advance or report** — if both pass, advances the stage and records history;
   otherwise returns a clear, specific list of required changes.

A structured **pivot check** is included if you're changing direction: is the new
direction genuinely more promising, or are you avoiding a hard problem?

## Modes

- **MCP:** `crucible_advance_stage` (+ review/understanding tools).
- **File:** updates `state.json`, `stage_history.json`, `understanding_log/`.

## Related

- Run [`crucible:reviewer-round`](reviewer-round.md) first to de-risk the gate.
- [`crucible:understand`](understand.md) for ad-hoc understanding checks.
