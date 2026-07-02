# Security Policy

## Supported versions

Crucible is pre-1.0 and released from `main`. Security fixes are applied to the
latest released version only.

| Version | Supported |
| ------- | --------- |
| latest (`main` / newest release) | ✅ |
| older releases | ❌ |

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

Report privately via one of:

- GitHub's [private vulnerability reporting](https://github.com/vasanthsarathy/crucible/security/advisories/new)
  (Security → Report a vulnerability), or
- email **vsarathy@gmail.com** with subject line `SECURITY: crucible`.

Please include a description, reproduction steps, and the impact you observed.
You can expect an acknowledgement within a few days. Once a fix is available,
we'll coordinate disclosure and credit you (if you wish).

## Scope notes

- The optional MCP server makes outbound network requests to **arXiv** and
  **Semantic Scholar** for literature search. It does not transmit your project
  content to those services beyond the search queries you initiate.
- All project state is stored locally under `.crucible/` in your working directory.
