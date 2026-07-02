# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
