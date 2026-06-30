# Crucible

Review-driven Development (RDD) for AI/ML research papers.

The idea: run your work through a panel of adversarial reviewers at every stage, the same way TDD runs code through tests. You don't advance until the reviewers pass the work — and until you can explain it back without looking at the draft.

---

## Quick Start

```
/crucible:start
```

Claude will ask for your seed idea — a sentence, a question, an observation, anything. From there it runs a quick worthiness check (Flash + Copernicus gut-check: "is this worth pursuing?"), helps you articulate the idea, and orients you to the first real stage (PROBLEM).

From there, the loop is:

1. **Develop** the current stage with Claude's help
2. **`/crucible:reviewer-round`** — run the reviewer panel any time you want feedback
3. **`/crucible:advance`** — when ready to move on; triggers the formal gate + Socratic probe
4. **`/crucible:status`** — check where you are, what's open, what the reviewers said last

---

## Workflow Stages

```
SEED → PROBLEM → SURVEY → SOLUTION → DEVELOP → PAPER
         ↑gate↑   ↑gate↑   ↑gate↑    ↑gate↑    ↑gate↑
```

| Stage | What you're building | Gate question |
|---|---|---|
| **SEED** | Articulate the starting idea | No gate — Flash + Copernicus worthiness check only |
| **PROBLEM** | Precise problem definition, why it's hard, what a solution looks like | Are reviewers convinced this is a real, important, hard problem? |
| **SURVEY** | Literature map, gaps, Field Assumption Scanner | Have you done the scholarship and found a genuine contribution space? |
| **SOLUTION** | Approach sketches including failed ones, math in LaTeX | Is there at least one credible solution direction with clear rationale? |
| **DEVELOP** | Formal definitions, theorem/proof sketches, experiment designs and scripts | Is the formal development rigorous? Does the experimental evidence hold? |
| **PAPER** | Full draft assembled from all sections | Is this ready to submit to the target venue? |

---

## Skills

| Skill | When to use |
|---|---|
| `/crucible:start` | Begin a new project from a seed idea |
| `/crucible:reviewer-round` | Run the reviewer panel on current work (any time, not just at gates) |
| `/crucible:advance` | Trigger the formal gate check and advance to the next stage |
| `/crucible:understand` | Ad-hoc Socratic check on any concept in the project |
| `/crucible:status` | Dashboard: current stage, section progress, last reviewer verdicts, open concerns |

---

## Reviewer Panel

Seven personas evaluate every gate. Each has a fixed lens and default stance designed to resist sycophancy — they look for reasons to reject before reasons to accept.

| Reviewer | Lens | Default stance | Vote? |
|---|---|---|---|
| **Flash** | 60-second scan | Rejects by default. Needs one sentence it hasn't seen before. | Yes (INTRIGUED or REJECT) |
| **Archimedes** | Theory and rigor | Pedantic. Flags every hand-wave. Demands proof sketches. | Yes |
| **Edison** | Empirical evidence | Skeptical of results without ablations. Reproducibility focus. | Yes |
| **Copernicus** | Significance and novelty | Impatient with "we extend X to Y". Would this change how people think? | Yes |
| **Orwell** | Clarity and presentation | Demands plain English. Hostile to obfuscation. | Yes |
| **Linnaeus** | Scholarship and positioning | Encyclopedic. Finds the paper you missed. Uses live search. | No — findings only |
| **Socrates** | Assumption auditing | Assumes every claim has an unstated condition. | No — findings only |

### Gate threshold

**To pass a gate:** at least 3 of the 5 voting reviewers (Flash, Archimedes, Edison, Copernicus, Orwell) must give accept or revise — no outright reject.

Linnaeus and Socrates always produce required revisions regardless of the vote. Their findings must be addressed before advancing.

Every gate is preceded by a **Devil's Advocate pass** — Claude argues as hard as possible against the contribution before the panel evaluates it. The work must survive the worst-faith reading.

### Socratic probe

After passing the reviewer gate, you must answer 2-3 open-ended questions before the stage advances. Examples:

- PROBLEM → *"Explain in your own words why a naive approach to this problem fails."*
- SOLUTION → *"Walk me through the core insight of your solution sketch without looking at the draft."*
- PAPER → *"How would you explain the main contribution to a researcher from an adjacent field in two minutes?"*

Gaps are logged. The stage doesn't advance until you can demonstrate genuine understanding.

---

## State

All state lives in `.crucible/<project-id>/` in your working directory as plain Markdown and JSON files. Version-controllable. No server required.

```
.crucible/
  <project-id>/
    state.json              ← stage, venue, timestamps
    sections/               ← abstract.md, problem.md, survey.md, ...
    experiments/            ← runnable Python scripts + results
    review_rounds/          ← every reviewer round as JSON
    understanding_log/      ← Socratic probe history
    assumptions_log.json    ← surfaced assumptions (feeds Limitations section)
    ideas_log.json          ← captured tangents and future directions
    stage_history.json
    concepts.json           ← concept map (encountered → explained → applied)
```

---

## Installation

### Skills only (no server needed)

Install once, available in all projects:

```
/plugin install /path/to/crucible
```

Or if published to the plugin registry:

```
/plugin install crucible
```

### With the optional MCP server

The MCP server adds structured state queries, cross-session concept tracking, and live arXiv/Semantic Scholar search. Skills auto-detect it and delegate when available — they fall back to flat-file mode transparently if the server isn't running.

If you install the plugin via `/plugin install`, the bundled `plugin.json` already wires up the MCP server with `uv run` — you only need to build the environment once (step 1). The manual `.mcp.json` snippet (step 2) is for standalone use outside the plugin.

**1. Build the server environment** (one time, inside the plugin directory):

```bash
cd mcp-server && uv sync
```

**2. (Standalone only) Add to your project's `.mcp.json`:**

```json
{
  "mcpServers": {
    "crucible": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/crucible/mcp-server", "crucible"],
      "env": {
        "CRUCIBLE_DIR": ".crucible"
      }
    }
  }
}
```

Using `uv run` keeps this cross-platform (Windows, macOS, Linux) — no need to reference the platform-specific venv binary path. Requires [`uv`](https://docs.astral.sh/uv/) on your `PATH`.

`CRUCIBLE_DIR` controls where state is written. Defaults to `.crucible` in the current directory if not set.

---

## Venue profiles

The reviewer panel adjusts weighting based on your target venue. Set a venue when starting a project or update it in `state.json`. Built-in profiles:

`NeurIPS` · `ICLR` · `ICML` · `ACL` · `EMNLP` · `CVPR` · `AAAI` · `Nature` · `TMLR`

ICLR weights Archimedes and Edison highest (reproducibility). Nature weights Copernicus highest (broad significance required). TMLR weights Edison highest and Flash lower (thoroughness over novelty framing).

---

## Tips

- **Run `/crucible:reviewer-round` often** — not just at gates. Early feedback is cheap.
- **Use the ideas log** — if a tangent or new direction occurs to you mid-project, capture it without derailing: "log this idea: [...]". It goes to `ideas_log.json` for later.
- **Linnaeus uses live search** — at SURVEY and PAPER stages, it searches arXiv and Semantic Scholar for recent related work. This is the main defense against accidentally reinventing something.
- **Pivot evaluation** — if you want to significantly change direction, `/crucible:advance` includes a structured pivot check before committing: is the new direction genuinely more promising, or are you avoiding a hard problem?
- **The understanding log is evidence** — the full arc from SEED to PAPER (gaps at each stage, when they closed) documents that the paper is genuinely yours.
