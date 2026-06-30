---
name: crucible:understand
description: Ad-hoc Socratic understanding check on any concept from your current research project. Use when you realize mid-session that you're not sure about something. Logs gaps and clarifications.
---

# Understanding Check

You are running an ad-hoc understanding probe. The researcher wants to verify or deepen their understanding of a specific concept.

## Step 0: Check for MCP

Look for `crucible_log_understanding_check` in your available tools.
- **MCP mode**: use MCP tool to log the understanding check.
- **File mode**: write understanding check directly to `.crucible/<project-id>/understanding_log/<timestamp>-adhoc.json`.

## Step 1: Identify the Concept

Ask: "What concept do you want to check your understanding of?"

Wait for their response. It might be something like "the convergence proof in my method", "what IID actually means for my setup", "why my baseline is the right comparison", etc.

## Step 2: Probe (Socratic Style)

Ask one targeted open-ended question that requires the researcher to reconstruct the concept from first principles — not recall a definition, but demonstrate understanding:

Good question forms:
- "Explain [concept] in your own words — what's the core idea?"
- "Walk me through why [concept] matters for your specific problem."
- "If [concept] didn't hold, what would break in your approach?"
- "How would you explain [concept] to a master's student who hasn't seen it before?"

Ask only one question. Wait for the full response.

## Step 3: Assess

Assess the response:
- **Clear:** researcher articulates the concept correctly and at the right level of precision
- **Partial:** researcher has the gist but misses a key aspect or conflates two things
- **Gap:** researcher cannot explain it or gets it materially wrong

## Step 4: Respond

**If clear:**
"You've got this. [One sentence confirming what they demonstrated.] [Optional: one extension question if relevant — 'One thing worth also knowing: ...'.]"

**If partial:**
"You have the main idea. The part that needs sharpening: [explain the missing piece precisely]. Does that land?"
Re-ask a slightly different form of the question to confirm.

**If gap:**
"Let me explain this properly. [2–4 paragraph explanation of the concept at the right level for the researcher — precise but not condescending.] Now try again: [restate the question]."

## Step 5: Log

Write to `.crucible/<project-id>/understanding_log/<YYYY-MM-DD-HHMMSS>-adhoc.json`:
```json
{
  "check_id": "<timestamp>",
  "stage": "<current_stage from state.json>",
  "concept": "<concept name>",
  "question": "<question asked>",
  "answer": "<researcher's answer>",
  "assessment": "clear|partial|gap",
  "gaps": ["<gap if any>"],
  "timestamp": "<ISO 8601 UTC>"
}
```

In MCP mode: call `crucible_log_understanding_check(...)`.
