# Design spec: evidence-grounded reviewer-persona overhaul

**Status:** draft for review · **Date:** 2026-07-02 · **Scope:** `crucible-rdd`

## 1. Goal

Recalibrate Crucible's reviewer personas and the stage gate so they reflect how
top ML/NLP venues (NeurIPS, ICLR, ICML, ACL/ARR — 2025, +ICLR 2026) *actually*
evaluate papers. Three goals, all approved:

1. **Recognize excellence** — the personas today only know how to find reasons to
   reject. Give them positive taste: what *excellent* looks like through each lens.
2. **Calibrate standards** — ground each persona's bar in real venue rubrics.
3. **Rethink the lineup** — fix coverage gaps (honesty, reproducibility, ethics,
   advocacy) and the gate mechanism.

## 2. Evidence basis (the taste model)

From the official 2025 reviewer forms/guidelines + real reviews of award papers:

1. **Soundness ⊥ Excitement.** ARR scores them separately; NeurIPS splits Quality
   from Significance. A paper can be sound-but-unexciting or exciting-but-unsound.
2. **Judge the paper's own claims.** ARR bans (H1–H17) the reflexes: not-novel,
   not-SOTA, too-simple, unsurprising, "could also run X", limitations-as-weakness.
   ICLR: "lack of SOTA does not by itself constitute grounds for rejection."
3. **Reward intellectual honesty.** A NeurIPS 2025 *negative result* won an award;
   honest limitations are a strength. ICML awards went to non-SOTA, precisely-scoped work.
4. **The "nugget" + elegance.** One crisp memorable insight; simplicity = beauty.
5. **Rigor bound to claims** — error bars, seeds, controls, stated assumptions.
6. **Reproducibility, ethics, artifacts** are first-class, *separate* dimensions.
7. **Taste lives in the meta-reviewer layer:** weigh arguments, never average scores;
   discount vague/low-confidence negativity; escalating bar to overturn consensus.
8. **Guard against LLM-reviewer pathologies:** sycophancy, prestige bias,
   phrasing-sensitivity, rating inflation (our reviewers *are* LLMs).

Sources: aclrollingreview.org/reviewerguidelines + /acguidelines · neurips.cc/
Conferences/2025/ReviewerGuidelines · icml.cc/Conferences/2025/ReviewerInstructions ·
iclr.cc/Conferences/2026/ReviewerGuide · venue award blogs (NeurIPS/ICLR 2025-26).

## 3. Schema changes (`models.py`)

Add to `ReviewerPersona` (all with backward-compatible defaults so existing stored
custom personas still deserialize):

- `axis: Literal["soundness", "significance", "cross_cutting"]` (default `cross_cutting`)
- `role: Literal["reviewer", "champion", "ethics"]` (default `reviewer`)
- `excellence_signal: str` (default `""`) — what excellent looks like through this lens
- `anti_heuristics: list[str]` (default `[]`) — banned reflexes this persona must not use

Add a shared constant `ANTI_HEURISTICS` (the ARR H1–H17 list, condensed) referenced
by personas and the gate.

## 4. Recalibrated personas (`reviewer_personas.py`)

All 7 kept; `default_stance` reframed from "rejects by default" to *demanding-but-fair*.

| id | axis | excellence_signal | anti-heuristics removed |
|---|---|---|---|
| **flash** | significance | one crisp, memorable "nugget"; a simple idea that reframes | reject-for-unsurprising (H1); pattern-match "incremental" |
| **archimedes** | soundness | proofs the reviewer verifies; assumptions explicit; mechanism/"why" | demand complexity, treat simplicity as weakness (H7); flag without naming the gap |
| **edison** | soundness | experiments track claims; error bars/seeds/controls; reproducible; honest generalization | reject-for-not-SOTA (H5); "could also run X" as dealbreaker (H13); demand closed-model comparison (H14) |
| **copernicus** | significance | others will build on it; reframes/unifies; simplicity=beauty; insight & efficiency count | "not novel"/"extends X to Y" without a citation (H3); complexity-as-contribution |
| **orwell** | cross_cutting | self-contained exposition that answers the reader's questions; contribution as a refutable claim up front | penalize writing polish over content (H11); reward jargon |
| **linnaeus** | cross_cutting | fair positioning; credits "novel combination of known techniques" | "missing citation" for <3-month-old/non-archival work (H12); novelty complaint without naming prior work; citation-count as validity (H17) |
| **socrates** *(recast → intellectual honesty)* | cross_cutting | claims calibrated to evidence; assumptions surfaced; honest limitations rewarded; negative results valued | treat a stated limitation as a weakness (H16); penalize candor |

Full `evaluation_focus` / `default_stance` prose for each written during implementation,
following these signals.

## 5. New voices

- **Champion** (`role="champion"`, non-voting, `axis=significance`). Proposed name
  **Cicero**. Surfaces the strongest *honest* case FOR the work — the nugget, who
  will build on it, why it matters. ARR names "champion reviewers" as a real signal.
  Anti-heuristics: no sycophancy; never champion work with a fatal soundness flaw.
- **Ethics flag** (`role="ethics"`, non-voting, `axis=cross_cutting`). Proposed name
  **Rawls**. Flags data/consent, dual-use/abuse, fairness/harms, honest broader impact.
  **Non-punitive** — "answering no is not grounds for rejection"; raises an
  ethics-review flag, never auto-sinks a paper. No independent legal judgments.

## 6. Gate rework (`advance.md`) — the highest-leverage change

Replace the **"3-of-5 voting reviewers accept/revise"** threshold with a reasoned
**area-chair meta-review synthesis** (proposed role name **the Chair / Athena**),
because every venue instructs ACs to weigh arguments, *not average scores*:

1. Collect all reviewer outputs, the Champion's case, and any Ethics flags.
2. Produce **two separate verdicts** — a **soundness** verdict and a
   **significance/excitement** verdict — never collapsed.
3. **Weigh substantiated arguments, not counts.** A specific, load-bearing soundness
   fault (broken proof, unsupported main claim) is a dealbreaker even if only one
   reviewer raised it. **Discount vague or low-confidence negativity**, and **discard
   objections that are banned heuristics** (not-novel-without-citation, not-SOTA,
   too-simple, could-also-run-X, limitations-as-weakness).
4. **Reward honesty:** candor and precise scoping must not lower the verdict.
5. **Consider the Champion's case explicitly;** address Ethics flags (acknowledge/
   mitigate) without treating an honest impact statement as grounds to block.
6. **Advance when:** no unresolved dealbreaker soundness fault AND the significance
   verdict clears the venue's bar. Output a meta-review (reasons to advance, decisive
   concerns, required revisions) — not a tally.
7. **Escalating bar:** to block sound work with a strong champion, the blocking
   concern must be specific and load-bearing ("at the level of a full review").

The Socratic understanding probe after the gate is unchanged.

## 7. Venue emphasis refresh (`venue_profiles.py`)

Reinterpret per-reviewer weights as **emphasis hints the Chair applies** (not vote
multipliers), refreshed to real venue values and extended to the new voices:

- **NeurIPS** — significance *co-equal* with soundness; reproducibility & honesty emphasized.
- **ICLR** — contribution-dominant; clarity scored; rebuttal responsiveness valued.
- **ICML** — theory+empirics balance; claim-calibration foregrounded.
- **ACL/EMNLP (ARR)** — soundness ⊥ excitement made explicit; ethics & reproducibility first-class.
- **TMLR** — soundness over excitement (Flash down-weighted).
- **CVPR / AAAI / Nature** — kept, tuned; flagged as inferred (not open-review).

## 8. Skill mirroring (file-mode)

The personas/gate are embodied in skills for no-MCP mode; mirror all changes in:
- `skills/crucible-reviewer-round.md` — new persona definitions, excellence signals,
  anti-heuristics, Champion + Ethics voices, two-axis output.
- `skills/crucible-advance.md` — the meta-review synthesis gate (replaces the vote).
- `skills/crucible-start.md` — worthiness check uses recalibrated Flash + Copernicus.

## 9. Cross-cutting: LLM-reviewer-pathology guards

Bake into every persona + the Chair: no sycophancy; ignore author prestige/framing;
judge substance over phrasing; resist rating inflation. State these explicitly in the
reviewer-round + advance skills.

## 10. Files touched

`models.py` · `reviewer_personas.py` · `venue_profiles.py` · `skills/crucible-reviewer-round.md`
· `skills/crucible-advance.md` · `skills/crucible-start.md` · README + docs persona tables
· tests: `test_personas.py` (new fields, new voices), `test_models.py`, `test_server.py`.

## 11. Testing

- Personas expose the new fields with valid values; `flash`/`edison`/`copernicus`
  no longer carry reject-by-default stances.
- Champion and Ethics personas present with correct `role`/`is_voting`.
- Backward compat: a stored persona JSON without the new fields still deserializes.
- Gate logic is skill-driven (prose), so it's validated by review, not unit tests;
  add a fixture documenting an expected meta-review shape.

## 12. Out of scope (YAGNI)

- No new MCP tools; no change to state-file layout.
- CVPR/AAAI/Nature taste stays inferred (not open-review; low ROI to deepen now).
- No automated OpenReview scraping at runtime.

## 13. Open naming decisions (confirm during review)

- Champion = **Cicero**? · Ethics = **Rawls**? · Chair/meta-reviewer = **Athena**?
