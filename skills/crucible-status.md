---
name: crucible:status
description: Show the current state of your research project — stage, section completion, last reviewer round results, open concerns, concept gaps, and recent ideas.
---

# Research Project Status

You are rendering a status dashboard for the active research project.

## Step 0: Find Active Project

Check for MCP (`crucible_list_projects`). If no MCP:
- List directories in `.crucible/`
- If one project: use it
- If multiple: ask "Which project? [list names from state.json files]"
- If none: "No projects found. Run `crucible:start` to begin."

## Step 1: Read State

Read (or query via MCP):
- `state.json` — project id, name, stage, venue, created_at
- `sections/<name>.md` — check each for content (non-empty = exists)
- `review_rounds/*.json` — find the most recent round
- `understanding_log/*.json` — find any gaps not yet resolved
- `assumptions_log.json` — count unresolved assumptions
- `ideas_log.json` — last 3 entries
- `concepts.json` — find concepts with status `encountered` (not yet `explained`)

## Step 2: Render Dashboard

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROJECT: <name>  [<project-id>]
Target venue: <venue | "not set">
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STAGE: <current_stage>
Progress: SEED → PROBLEM → SURVEY → SOLUTION → DEVELOP → PAPER
          [mark completed stages with ✓, current with →, future with ·]

SECTIONS
  ✓ abstract        (has content)
  ✓ problem         (has content)
  · survey          (empty)
  · solution        (empty)
  · method          (empty)
  · experiments     (empty)
  · results         (empty)
  · related_work    (empty)
  · conclusion      (empty)

LAST REVIEWER ROUND  [<round timestamp | "none yet">]
  Flash:       <verdict | "—">
  Archimedes:  <verdict | "—">
  Edison:      <verdict | "—">
  Copernicus:  <verdict | "—">
  Orwell:      <verdict | "—">
  Linnaeus:    <N> required revisions
  Socrates:    <N> surfaced assumptions

OPEN CONCERNS
  <list top 3 unresolved concerns from last round, or "None" if clear>

UNDERSTANDING MAP
  Concepts to revisit (encountered but not yet explained):
    · <concept>
    · <concept>
  (Run `crucible:understand` to check understanding of any concept)

RECENT IDEAS
  <last 3 ideas_log entries with dates, or "No ideas logged yet">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next: <one sentence on what to work on now given the current stage and open concerns>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
