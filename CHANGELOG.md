# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-03

### Added
- Engineering rigor: `ruff` (lint + format) and `mypy` config, both enforced in CI
  and via a `.pre-commit-config.yaml`.
- Contributor infrastructure: `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  and GitHub issue / PR templates.
- Release automation: `scripts/bump-version.sh` keeps the version in sync across
  `plugin.json` and `marketplace.json`; the marketplace entry now carries `version`.
- Documentation: `docs/` with an architecture overview and a per-skill reference;
  a canonical seed-to-first-gate walkthrough in the plugin README.
- README demo placeholder (`assets/demo-placeholder.svg`) + `docs/recording-a-demo.md`.
- Two new reviewer voices — **Cicero**, a "champion" that argues the strongest honest
  case *for* the work, and **Rawls**, a non-punitive ethics & societal-impact flag —
  bringing the panel to nine personas.
- Every persona now carries an `excellence_signal` (what excellent work looks like
  through its lens) and `anti_heuristics` guardrails (illegitimate rejection reflexes
  it must not use), plus a soundness / significance `axis`.

### Changed
- **Reviewer personas recalibrated** to match how top venues (NeurIPS / ICLR / ICML /
  ACL 2025–26) actually evaluate papers: recognize excellence rather than only finding
  flaws; no reject-by-default stances; reward honest limitations; don't demand SOTA or
  novelty. (Grounded in a research pass over the venues' reviewer rubrics + real reviews
  of award papers.)
- **Stage gate reworked.** `/crucible:advance` now runs an area-chair meta-review
  synthesis (**Athena**) that produces two *separate* verdicts — soundness and
  significance — by weighing substantiated arguments, replacing the old "3 of 5
  reviewers" vote count.
- Venue profiles refreshed to the soundness / significance framing.
- Skill activation tuned so Claude auto-invokes the safe skills and leaves the
  stateful ones deliberate: `reviewer-round`, `understand`, and `status` now
  auto-invoke via scoped "use when…" descriptions; `start` and `advance` are
  explicit-only (`disable-model-invocation: true`) because they create project
  state / cross a stage gate.
- The `crucible_update_concept_status` MCP tool now validates the `stage` argument
  against the allowed stages (typed `Stage`) instead of accepting any string.
- Modernized reviewer/venue enums to `enum.StrEnum`.

## [0.1.0] - 2026-07-02

Initial public release.

### Added
- `crucible` plugin marketplace with its catalog (`.claude-plugin/marketplace.json`).
- `crucible-rdd` plugin: Review-Driven Development for AI/ML research papers.
  - Five skills: `start`, `reviewer-round`, `advance`, `understand`, `status`.
  - Seven-persona adversarial reviewer panel (Flash, Archimedes, Edison,
    Copernicus, Orwell, Linnaeus, Socrates) with staged gates: SEED → PROBLEM →
    SURVEY → SOLUTION → DEVELOP → PAPER.
  - Socratic understanding probes that block stage advancement.
  - Plain-file state under `.crucible/` (Markdown + JSON, no server required).
  - Optional MCP server: structured state queries, cross-session concept
    tracking, and live arXiv / Semantic Scholar search.
  - Built-in venue profiles (NeurIPS, ICLR, ICML, ACL, EMNLP, CVPR, AAAI,
    Nature, TMLR).
- Styled marketplace + plugin READMEs, monochrome/burnt-ember logo, MIT license,
  and CI (manifest validation + 25 passing MCP-server tests).

[Unreleased]: https://github.com/vasanthsarathy/crucible/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/vasanthsarathy/crucible/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/vasanthsarathy/crucible/releases/tag/v0.1.0
