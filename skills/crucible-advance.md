---
name: crucible:advance
description: Check readiness to advance to the next research stage. Runs a full reviewer gate, then a Socratic understanding probe. Advances if both pass; returns a clear list of required changes if not.
---

# Advancing to the Next Stage

You are checking whether the researcher is ready to advance from their current stage. Two gates must pass: (1) reviewer panel gate, (2) Socratic understanding probe.

## Step 0: Check for MCP

Look for `crucible_advance_stage` in your available tools.
- **MCP mode**: use MCP tools for state reads and the advance call.
- **File mode**: read/write `.crucible/<project-id>/` files directly.

## Step 1: Read Current State

Read `state.json`. Identify:
- Current stage (e.g., `PROBLEM`)
- Next stage (see progression below)
- Which sections have content

Stage progression:
```
SEED → PROBLEM → SURVEY → SOLUTION → DEVELOP → PAPER
```

If current stage is `PAPER`, tell the researcher: "You're at the final stage. Use `crucible:reviewer-round` to run a final review. When reviewers pass, the paper is ready for submission prep."

## Step 2: Stage Gate Criteria

Before running the reviewer round, state the specific gate criteria for the current stage:

**PROBLEM gate:** Reviewers must believe this is a real, important, hard problem worth solving. `problem.md` must exist and be substantive. The problem must be formally defined (mathematical or computational precision).

**SURVEY gate:** Reviewers must be convinced the researcher has done the scholarship and can position a genuine contribution. `survey.md` must exist. Linnaeus must find no egregious missing citations. Field Assumption Scanner must have run (see below).

**SOLUTION gate:** Reviewers must see at least one credible solution direction with a clear rationale for why it addresses the problem. `solution.md` must exist with at least one concrete approach sketched.

**DEVELOP gate:** Reviewers must accept the rigor of the formal development and the experimental evidence. `method.md` and at least one of `experiments.md`/`results.md` must exist. Any theoretical claims must have proof sketches.

**PAPER gate:** All sections must have substantive content. Reviewers must accept the paper as suitable for submission to the target venue.

## Step 3: Field Assumption Scanner (SURVEY stage only)

If current stage is `SURVEY`, run the Field Assumption Scanner before the reviewer round:

Ask yourself: "What is this entire field assuming that nobody questions?" Scan the problem area for load-bearing assumptions the community accepts uncritically. These are the most promising targets for a transformative contribution.

Report 3–5 field-level assumptions, e.g.:
```
FIELD ASSUMPTION SCANNER
========================
The [field] assumes:
  1. [assumption] — consequence of challenging it: [consequence]
  2. [assumption] — consequence of challenging it: [consequence]
  3. [assumption] — consequence of challenging it: [consequence]

Any of these could be the foundation of a significant contribution.
Does your work challenge any of these? If so, that's worth making explicit.
```

Append this output to `.crucible/<project-id>/sections/survey.md` under a `## Field Assumptions` heading (or log via MCP).

## Step 4: Run Full Reviewer Gate Round

Run the complete reviewer round as defined in `crucible:reviewer-round` — all seven reviewers, Devil's Advocate pass, full structured feedback.

**Gate evaluation:**
Count votes from the five voting reviewers (Flash, Archimedes, Edison, Copernicus, Orwell):
- `accept` = 1 pass vote
- `revise` = 1 pass vote
- `reject` = 1 fail vote

Note: Flash uses INTRIGUED instead of ACCEPT — treat INTRIGUED as a pass vote in the gate count.

**Gate passes** if: ≥ 3 pass votes AND ≤ 2 reject votes.
**Gate fails** if: ≥ 3 reject votes.

Linnaeus and Socrates always produce required revisions. Even if the voting gate passes, their findings must be addressed before advancing (unless the researcher's advisor role overrides).

## Step 5: If Gate Fails — Return Required Changes

If the gate fails, produce:

```
GATE: FAIL (stage not advanced)
================================
Voting result: [N/5 pass votes]
Reviewers who rejected: [list]

REQUIRED BEFORE RETRYING:
  Critical (must fix):
    - [specific action from rejecting reviewers]
    - [specific action]
  
  Recommended (address to strengthen):
    - [suggestion from revise reviewers]
    - [suggestion]

Linnaeus required revisions: [N items — list them]
Socrates required disclosures: [N items — list them]

Come back with crucible:advance after addressing these.
```

Do not advance the stage. Do not modify `stage_history.json`.

## Step 6: If Gate Passes — Run Socratic Probe

Congratulate the reviewer gate result, then say: "Before we advance, I want to make sure you've genuinely internalized this stage's work. I'll ask you a few questions — answer in your own words without looking at the draft."

Ask the stage-appropriate questions below, **one at a time**. Wait for the response before asking the next.

**PROBLEM stage probe:**
1. "Explain in your own words why a naive or obvious approach to this problem fails. What's the specific obstacle?"
2. "If someone asked you at a conference why this problem matters, what would you say in 30 seconds?"
3. "What would a correct solution look like — what properties would it have?"

**SURVEY stage probe:**
1. "Which paper is most directly competitive with your planned contribution, and why is your approach different?"
2. "What assumption is the closest prior work making that you are not making (or vice versa)?"

**SOLUTION stage probe:**
1. "Walk me through the core insight of your solution sketch. Why does it work where naive approaches fail?"
2. "What is the riskiest assumption your solution is making? What happens if it doesn't hold?"

**DEVELOP stage probe:**
1. "What does your key experiment show that prior work could not have shown?"
2. "If your main result is correct, what should a reader do differently in their own work?"

**PAPER stage probe:**
1. "How would you explain the main contribution to a researcher from an adjacent field in two minutes?"
2. "What is the most important limitation of your work, and why is it not fatal to the contribution?"

**Assess each answer:**
- **Clear:** researcher articulates the concept correctly and precisely
- **Partial:** researcher gets the gist but misses a key aspect — clarify and re-ask
- **Gap:** researcher cannot explain it — pause, explain the concept, then re-ask

Log each probe to `.crucible/<project-id>/understanding_log/<timestamp>-<stage>-probe.json`:
```json
{
  "check_id": "<timestamp>",
  "stage": "<stage>",
  "question": "<question text>",
  "answer": "<researcher's answer>",
  "assessment": "clear|partial|gap",
  "gaps": ["<gap description if any>"],
  "timestamp": "<ISO 8601 UTC>"
}
```

**Probe passes** if all questions receive `clear` or `partial` assessments (gaps resolved through clarification).

## Step 7: If Probe Fails — Teach and Retry

If any question reveals a genuine gap that cannot be resolved in conversation, say:

```
UNDERSTANDING PROBE: INCOMPLETE
================================
You demonstrated understanding of: [topics]
Gap identified in: [topic]

Let me explain this before we advance.
[targeted explanation of the gap concept]

Try again: [repeat the question]
```

Do not advance until the probe passes.

## Step 8: Advance Stage

If both gate and probe pass:

1. Update `state.json`: set `current_stage` to `<next_stage>`, update `updated_at`.
2. Append to `stage_history.json`:
   ```json
   {"stage": "<next_stage>", "entered_at": "<ISO 8601 UTC now>"}
   ```
3. In MCP mode: call `crucible_advance_stage(project_id=<id>)`.

Then orient the researcher to the next stage:

```
ADVANCED TO: <NEXT_STAGE>
=========================
[2–3 sentences on what this stage involves and what sections to work on]

Key questions for this stage:
  - [question 1]
  - [question 2]

Run crucible:reviewer-round any time for feedback.
Run crucible:advance when you're ready to move forward.
```

---

## Pivot Evaluation

If the researcher says they want to significantly change direction (new problem, new approach that abandons the current one), run this before allowing the pivot.

Ask in order — wait for each answer:
1. "Is the new direction genuinely more promising, or is the current work getting hard and something shinier appeared?"
2. "Does the new direction incorporate what you've already learned on this project?"
3. "What specifically would you lose by pivoting? What would you carry forward?"

**After their answers, decide:**

**Commit to pivot** if: the new direction is demonstrably better informed by current learnings, and the researcher can articulate what they carry forward.
- Create a new project via `crucible:start` with the new seed
- Log the pivot decision

**Capture and continue** if: the new direction is genuinely interesting but not clearly better than completing the current work, or the researcher can't articulate what they'd carry forward.
- Log the idea via `crucible_log_idea` (MCP) or append to `ideas_log.json` (file mode)
- Tell the researcher: "Captured in your ideas log. Let's finish what we started."

**Log the evaluation** (MCP mode): call `crucible_log_pivot_evaluation(project_id, new_direction, outcome, rationale)`.

**Log the evaluation** (file mode): append to `.crucible/<project-id>/pivot_log.json`:
```json
{
  "eval_id": "<8-char hex>",
  "stage": "<current_stage>",
  "new_direction": "<description>",
  "outcome": "pivot|capture_and_continue",
  "rationale": "<your assessment>",
  "timestamp": "<ISO 8601 UTC>"
}
```
