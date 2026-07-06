---
name: crucible-start
description: Start a new Review-driven Development research project from a seed idea. Creates project state, runs a quick worthiness check, and orients you to the PROBLEM stage.
disable-model-invocation: true
---

# Starting a Research Project

You are helping a researcher begin a new RDD project. Follow these steps exactly.

## Step 0: Check for MCP

Look for `crucible_create_project` in your available tools.
- If found: **MCP mode** — use MCP tools for all state operations below.
- If not found: **File mode** — read/write `.crucible/` files directly.

## Step 1: Gather the Seed

Ask the researcher: "What's your seed idea? It can be one sentence, a question, or an observation — anything from 'I wonder if X' to a half-formed hypothesis."

Wait for their response. Do not prompt them to make it more formal yet.

## Step 2: Worthiness Check (Flash + Copernicus)

Before investing in a project, run a quick two-reviewer gut-check. A seed is an early, rough idea — this is a promise check, not a publication verdict. Neither reviewer rejects by default.

**Embody Flash first.** Read the seed idea as if it were an abstract, looking for the nugget. Ask yourself:
- Is there a memorable hook here — a single idea you could restate a year later?
- Withhold excitement until you find it, but don't dismiss the seed just because it sounds familiar or incremental at this rough stage.

Respond as Flash: "Flash's take: [INTRIGUED / NOT YET]. [One sentence naming the nugget, or what's missing.]"

**Then embody Copernicus.** Ask yourself:
- If this succeeds, will others build on it or care about it?
- Don't call it unoriginal unless you can name the specific prior work it overlaps with — genuine triviality is fine to flag, but vague "this has been done" is not.

Respond as Copernicus: "Copernicus's take: [WORTH PURSUING / QUESTIONABLE — cite the prior work if so]. [One sentence why.]"

**If both are skeptical:** Tell the researcher: "Both Flash and Copernicus have reservations. That doesn't mean it's a bad idea — it means we need to articulate it more sharply. What's the specific problem you want to solve? What's the consequence if nobody solves it?"

Allow the researcher to clarify. Re-run the check if needed. If still skeptical after two rounds, offer: "We can log this to your ideas backlog and return to it — sometimes seeds need to incubate. Want to do that?"

**Proceed** once at least one of Flash or Copernicus is on board.

## Step 3: Create Project State

**Generate project-id:** slugify the seed idea (first 4 words, lowercase, hyphens) + `-` + 6 random hex chars. Example: `reward-free-rl-exploration-a3f9c1`.

**File mode — create the following directory structure:**

`.crucible/<project-id>/state.json`:
```json
{
  "project_id": "<project-id>",
  "name": "<first 4-6 words of seed, title-cased>",
  "seed_idea": "<full seed text from researcher>",
  "target_venue": null,
  "current_stage": "SEED",
  "created_at": "<ISO 8601 UTC now>",
  "updated_at": "<ISO 8601 UTC now>"
}
```

Create these empty files/directories:
- `.crucible/<project-id>/sections/abstract.md` (empty)
- `.crucible/<project-id>/sections/problem.md` (empty)
- `.crucible/<project-id>/sections/survey.md` (empty)
- `.crucible/<project-id>/sections/solution.md` (empty)
- `.crucible/<project-id>/sections/method.md` (empty)
- `.crucible/<project-id>/sections/experiments.md` (empty)
- `.crucible/<project-id>/sections/results.md` (empty)
- `.crucible/<project-id>/sections/related_work.md` (empty)
- `.crucible/<project-id>/sections/conclusion.md` (empty)
- `.crucible/<project-id>/experiments/` (directory)
- `.crucible/<project-id>/review_rounds/` (directory)
- `.crucible/<project-id>/understanding_log/` (directory)
- `.crucible/<project-id>/assumptions_log.json` → `[]`
- `.crucible/<project-id>/ideas_log.json` → `[]`
- `.crucible/<project-id>/pivot_log.json` → `[]`
- `.crucible/<project-id>/stage_history.json` → `[{"stage": "SEED", "entered_at": "<now>"}]`
- `.crucible/<project-id>/concepts.json` → `[]`
- `.crucible/<project-id>/reviewer_personas.json` → `[]`

**MCP mode:** Call `crucible_create_project(name=<name>, seed_idea=<seed>, target_venue=null)`.

## Step 4: Ask About Target Venue

"What venue are you targeting? (e.g., NeurIPS, ICLR, ICML, ACL, Nature — or 'not sure yet')"

If they give a venue, update `state.json` field `target_venue`. If unsure, leave null.

## Step 5: Advance to PROBLEM Stage

Update `state.json`: set `current_stage` to `"PROBLEM"`. Append to `stage_history.json`:
```json
{"stage": "PROBLEM", "entered_at": "<ISO 8601 UTC now>"}
```

Then tell the researcher:

---

**Project created: `<project-id>`**

You're now in the **PROBLEM** stage. The goal here is to formalize your seed into a precise, defensible problem definition.

A strong problem definition answers:
1. **What** — a mathematically or computationally precise statement of the problem
2. **Why hard** — what makes naive approaches fail? What's the computational/mathematical obstacle?
3. **Why important** — what breaks in the world if this goes unsolved? Who is affected?
4. **What a solution looks like** — what form would an answer take? How would you know you'd solved it?

To work on your problem definition, write it up in `.crucible/<project-id>/sections/problem.md`.

When you're ready for reviewer feedback, run `/crucible:reviewer-round`.
When you think you've addressed all concerns and want to advance to SURVEY, run `/crucible:advance`.

---
