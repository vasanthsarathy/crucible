# Reviewer-Persona Overhaul — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recalibrate Crucible's reviewer personas and stage gate to reflect how top ML/NLP venues (NeurIPS/ICLR/ICML/ACL 2025-26) actually evaluate papers — positive taste, anti-heuristic guardrails, soundness⊥significance axes, a Champion and an Ethics flag, and a meta-review gate.

**Architecture:** Personas are Python data (`reviewer_personas.py`) typed by `models.py`, weighted per venue (`venue_profiles.py`), and mirrored in Markdown skills for file-mode. The stage gate lives in the `crucible-advance.md` skill (prose, not Python). This plan extends the schema, rewrites the persona data, refreshes venue emphasis, then mirrors everything into the skills.

**Tech Stack:** Python 3.11+, Pydantic v2, pytest, uv. Markdown skills.

## Global Constraints

- All MCP-server commands run from `plugins/crucible-rdd/mcp-server/` via `uv run --extra dev`.
- Quality gates (must pass before each commit): `ruff check`, `ruff format --check`, `mypy src`, `python -m pytest -q`.
- Keep internal "crucible" branding; do not rename package/tools/env vars.
- Backward compatibility: new `ReviewerPersona` fields MUST have defaults so stored custom-persona JSON (without them) still deserializes.
- Voting personas remain exactly 5 (flash, archimedes, edison, copernicus, orwell). Champion + Ethics are non-voting.
- Spec of record: `docs/specs/2026-07-02-reviewer-personas-redesign.md`.
- Proposed names (confirmed): Champion = **Cicero**, Ethics = **Rawls**, meta-reviewer = **Athena**.

---

### Task 1: Schema — axis, role, excellence_signal, anti_heuristics

**Files:**
- Modify: `plugins/crucible-rdd/mcp-server/src/crucible/models.py` (the `ReviewerPersona` model, ~line 98)
- Test: `plugins/crucible-rdd/mcp-server/tests/test_models.py`

**Interfaces:**
- Produces: `ReviewAxis = Literal["soundness", "significance", "cross_cutting"]`; `ReviewerRole = Literal["reviewer", "champion", "ethics"]`; `ReviewerPersona` gains `axis: ReviewAxis = "cross_cutting"`, `role: ReviewerRole = "reviewer"`, `excellence_signal: str = ""`, `anti_heuristics: list[str] = []`.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_models.py`:
```python
from crucible.models import ReviewerPersona


def test_reviewer_persona_new_fields_have_defaults():
    # Backward compat: legacy persona JSON lacks the new fields.
    p = ReviewerPersona.model_validate(
        {
            "reviewer_id": "legacy",
            "name": "Legacy",
            "lens": "x",
            "evaluation_focus": "y",
            "default_stance": "z",
        }
    )
    assert p.axis == "cross_cutting"
    assert p.role == "reviewer"
    assert p.excellence_signal == ""
    assert p.anti_heuristics == []


def test_reviewer_persona_accepts_new_fields():
    p = ReviewerPersona(
        reviewer_id="t",
        name="T",
        lens="l",
        evaluation_focus="e",
        default_stance="s",
        axis="soundness",
        role="champion",
        excellence_signal="great",
        anti_heuristics=["no SOTA reflex"],
    )
    assert p.axis == "soundness"
    assert p.role == "champion"
    assert p.anti_heuristics == ["no SOTA reflex"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --extra dev python -m pytest tests/test_models.py -q`
Expected: FAIL (unexpected/invalid fields, or attribute missing).

- [ ] **Step 3: Write minimal implementation**

In `models.py`, near the other type aliases (after `Stage = ...`):
```python
ReviewAxis = Literal["soundness", "significance", "cross_cutting"]
ReviewerRole = Literal["reviewer", "champion", "ethics"]
```
Replace the `ReviewerPersona` class with:
```python
class ReviewerPersona(BaseModel):
    reviewer_id: str
    name: str
    lens: str
    evaluation_focus: str
    default_stance: str
    axis: ReviewAxis = "cross_cutting"
    role: ReviewerRole = "reviewer"
    excellence_signal: str = ""
    anti_heuristics: list[str] = []
    is_voting: bool = True  # False for findings-only, champion, and ethics
    is_custom: bool = False  # True if added per-project
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --extra dev python -m pytest tests/test_models.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/crucible-rdd/mcp-server/src/crucible/models.py plugins/crucible-rdd/mcp-server/tests/test_models.py
git commit -m "feat(personas): add axis/role/excellence_signal/anti_heuristics fields"
```

---

### Task 2: Recalibrate the 7 personas + anti-heuristics constant

**Files:**
- Modify: `plugins/crucible-rdd/mcp-server/src/crucible/reviewer_personas.py`
- Test: `plugins/crucible-rdd/mcp-server/tests/test_personas.py`

**Interfaces:**
- Consumes: `ReviewerPersona` (Task 1).
- Produces: `ANTI_HEURISTICS: list[str]`; `BUILTIN_PERSONAS` with the 7 recalibrated personas carrying `axis`, `excellence_signal`, `anti_heuristics`, and reframed `default_stance` (no "rejects by default").

- [ ] **Step 1: Write the failing test**

Add to `tests/test_personas.py`:
```python
def test_no_persona_rejects_by_default():
    for p in BUILTIN_PERSONAS:
        assert "reject" not in p.default_stance.lower(), p.reviewer_id


def test_every_persona_has_excellence_and_axis():
    for p in BUILTIN_PERSONAS:
        assert p.excellence_signal, p.reviewer_id
        assert p.axis in {"soundness", "significance", "cross_cutting"}


def test_socrates_is_intellectual_honesty():
    socrates = next(p for p in BUILTIN_PERSONAS if p.reviewer_id == "socrates")
    assert "honest" in socrates.lens.lower() or "honest" in socrates.evaluation_focus.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --extra dev python -m pytest tests/test_personas.py -q`
Expected: FAIL (current stances contain "reject"; no excellence_signal).

- [ ] **Step 3: Write minimal implementation**

Add above `BUILTIN_PERSONAS` in `reviewer_personas.py`:
```python
# Illegitimate rejection reflexes (ACL/ARR H1-H17), shared by all personas + the gate.
ANTI_HEURISTICS: list[str] = [
    "Reject for unsurprising / obvious-in-hindsight results (H1)",
    "Call something 'not novel' without citing specific prior work (H3)",
    "Reject for not beating state-of-the-art (H5)",
    "Reject for negative results (H6)",
    "Reject for a method being 'too simple' (H7)",
    "Demand your own preferred methodology (H8)",
    "'The authors could also run experiment X' as grounds to reject (H13)",
    "Demand comparison to closed/proprietary models (H14)",
    "Treat a stated limitation as a weakness (H16)",
    "Treat citation count as validity (H17)",
]
```
Replace `BUILTIN_PERSONAS` with the 7 recalibrated personas:
```python
BUILTIN_PERSONAS: list[ReviewerPersona] = [
    ReviewerPersona(
        reviewer_id="flash",
        name="Flash",
        lens="60-second first impression",
        axis="significance",
        evaluation_focus="Is there one clear, memorable idea? Would an expert want to keep reading?",
        excellence_signal="A single crisp 'nugget' you could restate a year later; a simple idea that reframes a problem.",
        anti_heuristics=[
            "Reject for unsurprising results (H1)",
            "Pattern-match 'incremental' without reading the contribution",
        ],
        default_stance="Withholds excitement until it finds the nugget; does not dismiss work for mere familiarity.",
        is_voting=True,
    ),
    ReviewerPersona(
        reviewer_id="archimedes",
        name="Archimedes",
        lens="Theory and rigor",
        axis="soundness",
        evaluation_focus="Are claims proved rather than asserted? Are assumptions stated? Is the math correct?",
        excellence_signal="Proofs the reviewer can and did verify; assumptions explicit; theory that explains WHY, not just a bound.",
        anti_heuristics=[
            "Treat simplicity as weakness / demand complexity (H7)",
            "Flag a hand-wave without naming the exact unproven step",
        ],
        default_stance="Pedantic about specifics; every objection names the exact gap. Leans revise unless a load-bearing claim is unsupported.",
        is_voting=True,
    ),
    ReviewerPersona(
        reviewer_id="edison",
        name="Edison",
        lens="Empirical evidence and reproducibility",
        axis="soundness",
        evaluation_focus="Do experiments test the stated claims? Are baselines fair, variance reported, results reproducible?",
        excellence_signal="Experiments track the claims precisely; error bars / multiple seeds; controls that isolate mechanism; documented code and data; honest about generalization.",
        anti_heuristics=[
            "Reject for not beating SOTA (H5)",
            "'Could also run experiment X' as a dealbreaker (H13)",
            "Demand closed-model comparison (H14)",
        ],
        default_stance="Skeptical when claims outrun evidence; asks for the missing seed or baseline, but credits sufficient evidence for the claim actually made.",
        is_voting=True,
    ),
    ReviewerPersona(
        reviewer_id="copernicus",
        name="Copernicus",
        lens="Significance and contribution",
        axis="significance",
        evaluation_focus="Will others build on this? Does it reframe or unify a problem? Is the problem important?",
        excellence_signal="Work others will use or extend; reframes a problem or challenges an assumption and demonstrates it; simplicity read as beauty; insight and efficiency count as contributions.",
        anti_heuristics=[
            "Call something 'not novel' / 'extends X to Y' without citing specific prior work (H3)",
            "Mistake complexity for contribution",
            "Treat SOTA as significance",
        ],
        default_stance="Impatient with genuinely trivial deltas, but must name a specific prior work to call something incremental.",
        is_voting=True,
    ),
    ReviewerPersona(
        reviewer_id="orwell",
        name="Orwell",
        lens="Clarity and presentation",
        axis="cross_cutting",
        evaluation_focus="Is the contribution stated as a refutable claim up front? Can an expert follow and reproduce from the text?",
        excellence_signal="Self-contained exposition that anticipates the reader's questions; abstract states the contributions; a running example; clarity fused with reproducibility.",
        anti_heuristics=[
            "Penalize writing/language polish over content (H11)",
            "Reward jargon as sophistication",
        ],
        default_stance="Demands plain English and an up-front contribution; separates 'unclear' (dealbreaker) from typos (polish).",
        is_voting=True,
    ),
    ReviewerPersona(
        reviewer_id="linnaeus",
        name="Linnaeus",
        lens="Scholarship and positioning",
        axis="cross_cutting",
        evaluation_focus="Is prior work fairly cited and the contribution correctly positioned? Any essential missing references?",
        excellence_signal="Honest positioning that credits a 'novel combination of known techniques' as valuable without burying the contribution; complete, fair related work.",
        anti_heuristics=[
            "'Missing citation' for work under 3 months old or non-archival (H12)",
            "Novelty complaint without naming the prior work",
            "Treat citation count as validity (H17)",
        ],
        default_stance="Encyclopedic; surfaces the missed paper — but a novelty objection must name a specific published work. Produces findings, not a verdict.",
        is_voting=False,
    ),
    ReviewerPersona(
        reviewer_id="socrates",
        name="Socrates",
        lens="Assumptions and intellectual honesty",
        axis="cross_cutting",
        evaluation_focus="What is assumed but unstated? Are claims scoped precisely to the evidence? Are limitations honest?",
        excellence_signal="Claims calibrated to evidence; assumptions surfaced; limitations stated candidly (a strength, not a liability); negative results valued.",
        anti_heuristics=[
            "Treat a stated limitation as a weakness (H16)",
            "Penalize candor or honest scoping",
        ],
        default_stance="Assumes every claim has an unstated condition; rewards candor and precise scoping; flags overclaiming, not honesty. Produces findings, not a verdict.",
        is_voting=False,
    ),
]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --extra dev python -m pytest tests/test_personas.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/crucible-rdd/mcp-server/src/crucible/reviewer_personas.py plugins/crucible-rdd/mcp-server/tests/test_personas.py
git commit -m "feat(personas): recalibrate the 7 personas with excellence signals + anti-heuristics"
```

---

### Task 3: Add Champion (Cicero) + Ethics (Rawls)

**Files:**
- Modify: `plugins/crucible-rdd/mcp-server/src/crucible/reviewer_personas.py` (append to `BUILTIN_PERSONAS`)
- Test: `plugins/crucible-rdd/mcp-server/tests/test_personas.py`

**Interfaces:**
- Consumes: `ReviewerPersona` with `role` (Task 1).
- Produces: `BUILTIN_PERSONAS` length 9; `cicero` (role=champion), `rawls` (role=ethics), both non-voting.

- [ ] **Step 1: Update the failing tests**

Edit `tests/test_personas.py` — update the three count/id tests and add role tests:
```python
def test_nine_builtin_personas():
    assert len(BUILTIN_PERSONAS) == 9
    ids = {p.reviewer_id for p in BUILTIN_PERSONAS}
    assert ids == {
        "flash", "archimedes", "edison", "copernicus",
        "linnaeus", "orwell", "socrates", "cicero", "rawls",
    }


def test_voting_reviewers_count():
    voting = [p for p in BUILTIN_PERSONAS if p.is_voting]
    assert len(voting) == 5  # flash, archimedes, edison, copernicus, orwell


def test_non_voting_personas():
    non_voting = {p.reviewer_id for p in BUILTIN_PERSONAS if not p.is_voting}
    assert non_voting == {"linnaeus", "socrates", "cicero", "rawls"}


def test_champion_and_ethics_roles():
    by_id = {p.reviewer_id: p for p in BUILTIN_PERSONAS}
    assert by_id["cicero"].role == "champion"
    assert by_id["rawls"].role == "ethics"
    assert not by_id["cicero"].is_voting
    assert not by_id["rawls"].is_voting


def test_get_active_personas_returns_nine(tmp_path):
    store = ProjectStore(tmp_path / ".crucible")
    pid = store.create_project("Test", "seed")
    personas = get_active_personas(pid, store)
    assert len(personas) == 9
```
Delete the now-superseded `test_seven_builtin_personas`, `test_linnaeus_and_socrates_not_voting`, and the old `test_get_active_personas_returns_builtins_plus_custom`.

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --extra dev python -m pytest tests/test_personas.py -q`
Expected: FAIL (length 7, missing cicero/rawls).

- [ ] **Step 3: Write minimal implementation**

Append to `BUILTIN_PERSONAS` (before the closing `]`):
```python
    ReviewerPersona(
        reviewer_id="cicero",
        name="Cicero",
        lens="The strongest case for the work",
        axis="significance",
        role="champion",
        evaluation_focus="What is genuinely good here? Who will build on it? What is the best version of this contribution?",
        excellence_signal="Articulates the nugget and the paper's real strengths as a committed champion reviewer would.",
        anti_heuristics=[
            "Sycophancy — praise without substance",
            "Champion work that has a fatal, specific soundness flaw",
        ],
        default_stance="Advocates: surfaces the strongest honest case for acceptance. A signal to weigh, never a rubber stamp. Produces findings, not a verdict.",
        is_voting=False,
    ),
    ReviewerPersona(
        reviewer_id="rawls",
        name="Rawls",
        lens="Ethics and societal impact",
        axis="cross_cutting",
        role="ethics",
        evaluation_focus="Data collection and consent, dual-use / potential for abuse, fairness and harms to groups, honest broader impact.",
        excellence_signal="Risks acknowledged and addressed; responsible-research diligence.",
        anti_heuristics=[
            "Treat an honest broader-impact statement as grounds to reject",
            "Make independent legal judgments",
        ],
        default_stance="Raises an ethics-review flag when warranted; non-punitive — answering 'no' is not grounds for rejection. Produces findings, not a verdict.",
        is_voting=False,
    ),
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --extra dev python -m pytest tests/test_personas.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/crucible-rdd/mcp-server/src/crucible/reviewer_personas.py plugins/crucible-rdd/mcp-server/tests/test_personas.py
git commit -m "feat(personas): add Cicero (champion) and Rawls (ethics flag)"
```

---

### Task 4: Refresh venue emphasis

**Files:**
- Modify: `plugins/crucible-rdd/mcp-server/src/crucible/venue_profiles.py`
- Test: `plugins/crucible-rdd/mcp-server/tests/test_personas.py`

**Interfaces:**
- Consumes: nothing new.
- Produces: updated `VENUE_PROFILES` notes/weights; `get_venue_weights` fallback list unchanged (still the 7 scoring ids). Champion/ethics are signals, not weighted votes — they are NOT added to weight dicts.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_personas.py`:
```python
def test_venue_notes_mention_axes():
    # Notes should reflect the soundness/significance framing, not the old vote language.
    acl = VENUE_PROFILES["ACL"].notes.lower()
    assert "soundness" in acl and "excitement" in acl
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --extra dev python -m pytest tests/test_personas.py::test_venue_notes_mention_axes -q`
Expected: FAIL.

- [ ] **Step 3: Write minimal implementation**

Update the `notes` (and lightly the weights) for each profile in `venue_profiles.py` to the evidence-based framing. Minimum required edits (keep the existing weight dicts, adjust values shown):
- NeurIPS notes → `"Significance scored co-equal with soundness; reproducibility and honest limitations rewarded."` (set `copernicus` 1.3, `edison` 1.3).
- ICLR notes → `"Contribution-dominant; clarity is scored; rebuttal responsiveness valued. Soundness and rigor high."`
- ICML notes → `"Theory + empirics balance; claim calibration foregrounded."`
- ACL notes → `"Soundness and excitement scored separately; ethics and reproducibility first-class."` (raise `edison`/`linnaeus`).
- EMNLP notes → `"Like ACL: soundness vs excitement split; reproducibility emphasized."`
- TMLR notes → `"Soundness over excitement; correctness and thoroughness valued over novelty framing (Flash down-weighted)."`
- CVPR / AAAI / Nature notes → keep, append `" (taste inferred; not open-review)."`

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --extra dev python -m pytest tests/test_personas.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/crucible-rdd/mcp-server/src/crucible/venue_profiles.py plugins/crucible-rdd/mcp-server/tests/test_personas.py
git commit -m "feat(personas): refresh venue emphasis to soundness/significance framing"
```

---

### Task 5: Mirror personas into the reviewer-round skill (file-mode)

**Files:**
- Modify: `plugins/crucible-rdd/skills/crucible-reviewer-round.md`

*(Prose skill — validated by review, not unit tests.)*

- [ ] **Step 1: Rewrite the persona section**

Replace the seven-persona table/descriptions with the nine personas from Tasks 2-3, each listing: lens, **axis** (soundness / significance / cross-cutting), what it rewards (`excellence_signal`), and what it must NOT do (`anti_heuristics`). Add Cicero (champion) and Rawls (ethics) as non-voting voices.

- [ ] **Step 2: Add the two-axis output + guardrails**

Instruct the skill to (a) report a **soundness** read and a **significance/excitement** read separately per the axes; (b) obey the shared anti-heuristics list (paste the 10 `ANTI_HEURISTICS` items); (c) resist LLM-reviewer pathologies — no sycophancy, ignore author prestige/framing, judge substance over phrasing, resist rating inflation.

- [ ] **Step 3: Verify + commit**

Read the file end-to-end; confirm it names all 9 personas and both axes.
```bash
git add plugins/crucible-rdd/skills/crucible-reviewer-round.md
git commit -m "feat(skills): mirror recalibrated personas + axes into reviewer-round"
```

---

### Task 6: Rework the gate in the advance skill (file-mode)

**Files:**
- Modify: `plugins/crucible-rdd/skills/crucible-advance.md`

*(Prose skill — validated by review, not unit tests.)*

- [ ] **Step 1: Replace the vote threshold with meta-review synthesis**

Remove any "3 of 5 voting reviewers" / count-based rule. Add an **Area Chair (Athena)** synthesis step that:
1. Collects all reviewer outputs + Cicero's case + Rawls's flags.
2. Produces **two separate verdicts**: a soundness verdict and a significance/excitement verdict.
3. Weighs substantiated arguments, not counts; a specific load-bearing soundness fault is a dealbreaker even if raised once; **discounts vague/low-confidence negativity**; **discards objections that match the anti-heuristics list**.
4. Rewards honesty (candor must not lower the verdict); considers Cicero's case; addresses Rawls's flags non-punitively.
5. Advances when: no unresolved dealbreaker soundness fault AND the significance verdict clears the venue's bar. Outputs a meta-review (reasons to advance / decisive concerns / required revisions), not a tally.
6. Escalating bar: blocking sound, championed work requires a specific, load-bearing concern "at the level of a full review."

Keep the Devil's Advocate pass (before synthesis) and the Socratic probe (after) unchanged.

- [ ] **Step 2: Verify + commit**

Read end-to-end; confirm no count-based gate remains and the two-verdict synthesis is present.
```bash
git add plugins/crucible-rdd/skills/crucible-advance.md
git commit -m "feat(skills): replace vote gate with area-chair meta-review synthesis"
```

---

### Task 7: Recalibrate the worthiness check in the start skill

**Files:**
- Modify: `plugins/crucible-rdd/skills/crucible-start.md`

*(Prose skill — validated by review, not unit tests.)*

- [ ] **Step 1: Update the Flash + Copernicus worthiness gut-check**

Ensure the SEED worthiness check uses the recalibrated Flash (seeks the nugget, does not dismiss for familiarity) and Copernicus (needs a specific prior work to call something incremental). Frame it as "is there a promising nugget here?", not "reject unless surprising."

- [ ] **Step 2: Verify + commit**

```bash
git add plugins/crucible-rdd/skills/crucible-start.md
git commit -m "feat(skills): recalibrate worthiness check to seek the nugget"
```

---

### Task 8: Update docs + README persona tables

**Files:**
- Modify: `plugins/crucible-rdd/README.md` (Reviewer Panel table), `docs/reviewers.md` if present else `docs/architecture.md` gate section, `README.md` (root feature grid if it cites "seven personas").

- [ ] **Step 1: Update persona/gate documentation**

Reflect: 9 personas (7 recalibrated + Cicero + Rawls), the soundness⊥significance axes, and the meta-review gate (no longer "3 of 5"). Update any "seven personas" / "seven adversarial reviewers" copy to reflect the new panel and its positive-taste framing.

- [ ] **Step 2: Verify + commit**

```bash
git add plugins/crucible-rdd/README.md README.md docs/
git commit -m "docs: reflect recalibrated 9-persona panel and meta-review gate"
```

---

### Task 9: Full gate, changelog, release

**Files:**
- Modify: `CHANGELOG.md`; version via `scripts/bump-version.sh`.

- [ ] **Step 1: Run the full quality gate**

Run (from `plugins/crucible-rdd/mcp-server/`):
```bash
uv run --extra dev ruff check && uv run --extra dev ruff format --check && uv run --extra dev mypy src && uv run --extra dev python -m pytest -q
```
Expected: all pass.

- [ ] **Step 2: Bump version + changelog**

```bash
bash scripts/bump-version.sh 0.2.0
```
Add a `## [0.2.0]` CHANGELOG entry: "Evidence-grounded reviewer-persona overhaul — excellence signals + anti-heuristic guardrails, soundness⊥significance axes, Cicero (champion) and Rawls (ethics), and a meta-review gate replacing the vote threshold."

- [ ] **Step 3: Commit, tag, release**

```bash
git add -A
git commit -m "chore: release v0.2.0 — reviewer-persona overhaul"
git tag -a v0.2.0 -m "crucible-rdd v0.2.0"
git push origin main v0.2.0
gh release create v0.2.0 --title "v0.2.0 — reviewer-persona overhaul" --notes "See CHANGELOG."
```

---

## Self-Review

**Spec coverage:** §3 schema→Task 1; §4 personas→Task 2; §5 Champion/Ethics→Task 3; §6 gate→Task 6; §7 venues→Task 4; §8 skill mirroring→Tasks 5-7; §9 LLM guards→Task 5; §10 files/tests→Tasks 1-4,8; naming→Global Constraints. Covered.

**Placeholder scan:** Prose-skill tasks (5-7) specify exact content to write (personas, axes, gate steps) rather than "add appropriate X"; they are review-validated because Markdown skills have no unit-test harness. No TBDs.

**Type consistency:** `axis` values (`soundness`/`significance`/`cross_cutting`) and `role` values (`reviewer`/`champion`/`ethics`) are used identically across Tasks 1-4. Voting count stays 5; total personas 9.
