# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Engineering rigor: `ruff` (lint + format) and `mypy` config, both enforced in CI
  and via a `.pre-commit-config.yaml`.
- Contributor infrastructure: `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  and GitHub issue / PR templates.
- Release automation: `scripts/bump-version.sh` keeps the version in sync across
  `plugin.json` and `marketplace.json`; the marketplace entry now carries `version`.
- Documentation: `docs/` with an architecture overview and a per-skill reference.
- README demo placeholder (`assets/demo-placeholder.svg`) + `docs/recording-a-demo.md`.

### Changed
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

[Unreleased]: https://github.com/vasanthsarathy/crucible/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vasanthsarathy/crucible/releases/tag/v0.1.0
